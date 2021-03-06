#
# Script:    istcAdminHandler.py
# Version:   0.1
# Date:      ongoing
# Copyright: &copy; University of Liverpool 2009
# Description:
#           Administration Interface for ISTC
#
# Author(s): CS - Catherine Smith <catherine.smith@liv.ac.uk>
#
# Language:  Python
#
# Version History: 
# 0.01 - 25/06/2009 - CS - Everything needed for inital release

import cgitb
import codecs
import datetime
import os
import re
import smtplib
import sys
import time
import urllib

from copy import deepcopy
from crypt import crypt

# Site-packages
from lxml import etree

from mod_python import apache, Cookie
from mod_python.util import FieldStorage


from cheshire3.baseObjects import Session
from cheshire3.cqlParser import parse, SearchClause, Triple
from cheshire3 import exceptions as c3errors
from cheshire3.internal import cheshire3Root
from cheshire3.document import StringDocument
from cheshire3.marc_utils import MARC
from cheshire3.record import Record, LxmlRecord
from cheshire3.server import SimpleServer
from cheshire3.utils import flattenTexts
from cheshire3.web import www_utils
from cheshire3.web.www_utils import *

#from wwwSearch import *

from istcLocalConfig import *

dateRegex = re.compile('[\S]*-(([\d]*)-([\d]*)-([\d]*))T([\d]{2})([\d]{2})([\d]{2}).log')


class IstcAdminHandler:
    baseTemplatePath = os.path.join(cheshirePath, 'www', 'istc', 'html', 'baseTemplate.html')
    editNavPath = os.path.join(cheshirePath, 'www', 'istc', 'html', 'editNav.html')
    
    def __init__(self, lgr):
        self.logger = lgr

    def send_html(self, data, req, code=200):
        req.content_type = 'text/html; charset=utf-8'
        req.headers_out['Cache-Control'] = "no-cache, no-store"
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()      
    
        
    def send_pdf(self, data, req, code=200):
        req.content_type = 'application/pdf'
        req.send_http_header()
        req.write(data)
        req.flush()
        
        
    def show_adminMenu(self):
        page = read_file('adminmenu.html')
        page = page.replace('%USERS%', self.list_users())
        return page
 
    def _clear_dir(self, dir):
        # function to recursively clear an entire directory - dangerous if used incorrectly!!!
        # imitates "rm -rf dir/*" in shell
        for f in os.listdir(dir):
            fp = os.path.join(dir, f)
            if os.path.isdir(fp):
                if f <> 'preview':
                    try: os.shutil.rmtree(fp, ignore_errors=True)
                    except: pass
                else:
                    self._clear_dir(fp)

            else:
                os.remove(fp) 


    def list_users(self, values = None):
        global userStore
        if values == None:            
            values = {'%USERNAME%' : '',
                      '%FULLNAME%' : '',
                      '%EMAIL%' : '',
                      '%TELEPHONE%' : '',
                      '%USER%' : 'checked="true"',
                      '%SUPERUSER%' : ''
                      }
        lines = ['<h3>Current Users </h3>'
                 '<table class="currentusers">',
                 '<tr class="headrow"><td>Username</td><td>Real Name</td><td>Email Address</td><td>Telephone</td><td>Operations</tr>']

        for ctr, user in enumerate(userStore):
            uid = user.id
            if ((ctr+1) % 2): rowclass = 'odd'
            else:  rowclass = 'even'
            cells = '<td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (uid, user.realName, user.email, user.tel)
            cells = cells + '<td><a href="users.html?operation=delete&amp;userid=%s&confirm=true" class="fileop">DELETE</a></td>' % (uid)  

            lines.append('<tr class="%s">%s</tr>' % (rowclass, cells))
        lines.append('</table><br/>')

        lines.extend(['<h3>Add New User</h3>',
                         multiReplace(read_file('adduser.html'), values)
                        ])
        return '\n'.join(lines)
        #- end list_users()


    def add_user(self, form):
        page = read_file('adminmenu.html')
        
        values = {'%USERNAME%' : form.get('userid', ''),
                  '%FULLNAME%' : form.get('realName', ''),
                  '%EMAIL%' : form.get('email', ''),
                  '%TELEPHONE%' : form.get('tel', '')
                  }
        if (form.get('submit', None)):
            userid = form.get('userid', None)
            usertype = form.get('usertype', 'user')
            if not (userid and userid.isalnum()):
                if not userid:
                    message = 'Unable to add user - you MUST supply a username'
                else:
                    message = 'Unable to add user - username may only comprise alphanumeric characters.'
                values['%USERNAME%'] = ''
                values['%USER%'] = 'checked="true"'
                values['%SUPERUSER%'] = ''

                return page.replace('%USERS%', '<p class="error">%s</p>%s' % (message, self.list_users(values)))
            
            try:
                user = userStore.fetch_object(session, userid)
            except c3errors.ObjectDoesNotExistException:
                user = None
                
            if user is not None:
                values['%USERNAME%'] = ''
                values['%USER%'] = 'checked="true"'
                values['%SUPERUSER%'] = ''
                return page.replace('%USERS%', '<p class="error">User with username/id "%s" already exists! Please try again with a different username.</p>%s' % (userid, self.list_users(values)))
            else:
                # we do want to add this user
                if (usertype == 'superuser'):
                    userRec = xmlp.process_document(session, StringDocument(new_superuser_template.replace('%USERNAME%', userid)))
                    values['%SUPERUSER%'] = 'checked="true"'
                    values['%USER%'] = ''
                else :
                    userRec = xmlp.process_document(session, StringDocument(new_user_template.replace('%USERNAME%', userid)))
                    values['%USER%'] = 'checked="true"'
                    values['%SUPERUSER%'] = ''
                userNode = userRec.get_dom(session)
                passwd = form.get('passwd', None)
                # check password
                newHash = {}
                for f in session.user.simpleNodes:
                    if form.has_key(f):
                        newHash[f] = form.getfirst(f)
                passwd1 = form.get('passwd1', None)
                if (passwd1 and passwd1 != ''):
                    passwd2 = form.get('passwd2', None)
                    if (passwd1 == passwd2):
                        newHash['password'] = crypt(passwd1, passwd1[:2])
                    else:
                        
                        return page.replace('%USERS%', '<p class="error">Unable to add user - passwords did not match.</p>%s' % (self.list_users(values)))
       
                else:
                    return page.replace('%USERS%', '<p class="error">Unable to add user - password not supplied.</p>%s' % (self.list_users(values)))      
                
                # update DOM
                userNode = self._modify_userLxml(userNode, newHash)    
                self._submit_userLxml(userid, userNode)                    
                user = userStore.fetch_object(session, userid)
                values['%USERNAME%'] = ''
                values['%FULLNAME%'] = ''
                values['%EMAIL%'] = ''
                values['%TELEPHONE%'] = ''
                values['%USER%'] = 'checked="true"'
                values['%SUPERUSER%'] = ''
                return page.replace('%USERS%', self.list_users(values))
        return page.replace('%USERS%', self.list_users(values))
        #- end add_user()    


    def delete_user(self, form):
        global userStore, rebuild  
        page = read_file('adminmenu.html')             
        userid = form.get('userid', session.user.id) 
        cancel = form.get('cancel', None) 
        confirm = form.get('confirm', None)
        passwd = form.get('passwd', None)
        if (confirm == 'true'):
            output = ['<div id="maincontent"><h3 class="editheader">Delete User Confirmation.</h3>', read_file('deleteuser.html').replace('%USERID%', userid), '</div>']
            return ''.join(output)      
        elif (cancel == 'Cancel'):
            return page.replace('%USERS%', self.list_users())
        else:
            if (passwd and crypt(passwd, passwd[:2]) == session.user.password):                   
                try :
                    userStore.delete_record(session, userid)
                except :
                    return page.replace('%USERS%', '<p class="error">Unable to delete user %s - user does not exist.</p>%s' % (userid, self.list_users()))
                else :
                    rebuild = True
                    return page.replace('%USERS%', self.list_users())
            else :
                return page.replace('%USERS%', '<p class="error">Unable to delete user %s - incorrect password.</p>%s' % (userid, self.list_users()))

        #- end delete_user()





    def _modify_userLxml(self, userNode, updateHash):
        for c in userNode.iterchildren(tag=etree.Element):
            if c.tag in updateHash:
                c.text = updateHash[c.tag]
                del updateHash[c.tag]

        for k,v in updateHash.iteritems():
            el = etree.SubElement(userNode, k)
            el.text = v
            
        return userNode
        #- end _modify_userLxml() 


    def _submit_userLxml(self, id, userNode):
        rec = LxmlRecord(userNode)
        rec.id = id
        userStore.store_record(session, rec)
        userStore.commit_storing(session)
        #- end _submit_userLxml()

       
    def rebuild_database(self, form, req):
        req.content_type = 'text/html'
        req.send_http_header()
        head = unicode(read_file('header.html'))
        nav = unicode(read_file('editNav.html'))
        req.write(head)     
        req.write(nav)
        req.write('<div id="maincontent">')   
   
        if os.path.exists(lockfilepath) or os.path.exists(reflockfilepath) or os.path.exists(usalockfilepath) :
            req.write('<p><span class="error">[ERROR]</span> - Another user is already indexing this database. Please try again in 10 minutes.</p>\n<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')
        else :
            lock1 = open(lockfilepath, 'w')
            lock1.close() 
            lock2 = open(usalockfilepath, 'w')
            lock2.close() 
            lock3 = open(reflockfilepath, 'w')
            lock3.close()             
            try:
                self._clear_dir(os.path.join(dbPath, 'stores'))
                
                dbusa.clear_indexes(session)
                dbrefs.clear_indexes(session)
                db.clear_indexes(session)
                # now we've blitzed everything, we'll have to rediscover/build the objects
                build_architecture()
                
                #index usa
                usaProblems = 0
                session.database = dbusa.id
                error = False
                req.write('Loading and Indexing U.S.A. locations... ')
                usaRecordStore.begin_storing(session)
                dbusa.begin_indexing(session)
                try:
                    usaDocFac.load(session)
                    for doc in usaDocFac:
                        retval = usaBuildSingleFlow.process(session, doc)
                        if not isinstance(retval, Record): 
                            usaProblems += 1
                    if usaProblems > 0:
                        req.write('<span class="error">[ERROR]</span> - There were problems with %d entries<br/>\n' % usaProblems)
                except:
                    error = True
                    req.write('<span class="error">[ERROR]</span> - Indexing existed abnormally<br/>\n')
                usaRecordStore.commit_storing(session)
                dbusa.commit_indexing(session)
                dbusa.commit_metadata(session)
                if not error:
                    req.write('[<span class="ok"> OK </span>] <br />\n')
            
                #index refs
                refsProblems = 0
                session.database = dbrefs.id
                error = False
                req.write('Loading and Indexing bibliographical references... ')
                refsRecordStore.begin_storing(session)
                dbrefs.begin_indexing(session)
                try:
                    refsDocFac.load(session)
                    for doc in refsDocFac:
                        retval = refsBuildSingleFlow.process(session, doc)
                        if not isinstance(retval, Record): 
                            refsProblems += 1
                    if refsProblems > 0:
                        req.write('<span class="error">[ERROR]</span> - There were problems with %d entries<br/>\n' % refsProblems)
                except:
                    error = True
                    req.write('<span class="error">[ERROR]</span> - Indexing existed abnormally<br/>\n')
                refsRecordStore.commit_storing(session)
                dbrefs.commit_indexing(session)
                dbrefs.commit_metadata(session)
                if not error:
                    req.write('[<span class="ok"> OK </span>] <br />\n')
                    
                # rebuild and reindex main db
                req.write('Loading and Indexing records from %s<br/>\n' % sourceDir)
                recordStore.begin_storing(session)

                db.begin_indexing(session)
                # for some reason this doesn't work well in threads...
                start = time.time()

                problems = []
                session.database = db.id
                try:
                    baseDocFac.load(session)
                    # TODO: figure out how many files we're loading
                    req.write('<span id="rec-progress">Processing File: <span id="rec-count" style="font-weight:bold;font-size:larger;">0</span></span> ')                 
                    for x, doc in enumerate(baseDocFac):
                        req.write('<script type="text/javascript">e = document.getElementById("rec-count");e.innerHTML = "%d"\n</script><noscript>.</noscript>' % (x+1))
                        retval = buildSingleFlow.process(session, doc)
                        if not isinstance(retval, Record): 
                            problems.append((doc.filename, (retval)))
  
                    req.write('[<span class="ok"> OK </span>] <br />')
                    
                    req.write('Merging indexes...')
                    recordStore.commit_storing(session)
                    db.commit_indexing(session)
                    db.commit_metadata(session)
                    req.write('[<span class="ok"> OK </span>] <br />')
                    mins, secs = divmod(time.time() - start, 60)
                    hours, mins = divmod(mins, 60)
                    req.write('Indexing complete in %dh %dm %ds<br/>' % (hours, mins, secs))
                    
                    if len(problems):
                        req.write('<span class="error">The following file(s) were omitted due to errors that occured while loading: </span><br/>\n')
                        req.write('<br/>\n'.join(['%s - %s' % (p[0], p[1]) for p in problems]))
                        req.write('<br/>\n')
                        
                except:
                    # failed to complete - nothing else will work!
                    cla, exc, trbk = sys.exc_info()
                    excName = cla.__name__
                    try: excArgs = exc.__dict__["args"]
                    except KeyError: excArgs = str(exc)
                    #req.write('<span class="error">Indexing exited abnormally with message:<br/>\n%s</span>' % t.error) # thread version
                    req.write('<span class="error">Indexing exited abnormally:<br/>\n %s:%s</span>' % (excName, excArgs))
                   
            finally:
                if os.path.exists(lockfilepath):
                    os.remove(lockfilepath) 
                if os.path.exists(usalockfilepath):
                    os.remove(usalockfilepath) 
                if os.path.exists(reflockfilepath):
                    os.remove(reflockfilepath) 
                    
            req.write('<span class="ok">[OK]</span><br/>\n')    
            req.write('<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')
        foot = unicode(read_file('footer.html'))
        req.write('</div>')      
        req.write(foot)
        rebuild = True    

        
    def show_stats(self, file='searchhandler.log'):
        global dateRegex
        allstring = read_file(os.path.join(statspath, file))
        output = []
        regex = re.compile('searchhandler\S')
        files = os.listdir(statspath)
        files.sort(reverse=True)
        options= []
        for f in files :
            if(regex.match(f)):       
                date = re.findall(dateRegex, f)
                if (f == 'searchhandler.log' and f == file):
                    options.append('<option value="%s" selected="true">%s</option>' % (f, 'current'))
                elif (f == 'searchhandler.log'):
                    options.append('<option value="%s">%s</option>' % (f, 'current'))                                    
                elif (f == file):
                    options.append('<option value="%s" selected="true">%s-%s-%s</option>' % (f, date[0][1], date[0][2], date[0][3]))
                else :
                    options.append('<option value="%s">%s-%s-%s</option>' % (f, date[0][1], date[0][2], date[0][3]))
        if (file == 'searchhandler.log'):
            dateString = time.strftime("%Y-%m-%d %H:%M:%S")
        else :
            dateString = '%s %s:%s:%s' % (date[0][0], date[0][4], date[0][5], date[0][6])
        
        output.append('<h3>Statistics for period ending: <select id="fileNameSelect" value="1" onChange="window.location.href=\'stats.html?file=\' + this.value">%s</select></h3>' % ''.join(options))

        #start date
        start = re.match('^\n?\[(\d{4}-\d{2}-\d{2})', allstring)
        try:
            output.append('<h1>Statistics from %s to %s </h1><div class="statsdiv">' % (start.group(1), time.strftime('%Y-%m-%d')))
        except:
            output.append('<h1>Statistics from %s to %s </h1><div class="statsdiv">' % (time.strftime('%Y-%m-%d'), time.strftime('%Y-%m-%d')))

        #summary actions
        search = re.findall('STATS:search', allstring)
        browse = re.findall('STATS:browse', allstring)
        printrecs = re.findall('STATS:print', allstring)
        save = re.findall('STATS:save', allstring)
        email = re.findall('STATS:email', allstring)
        output.extend(['<h3>Full Counts</h3><table class="stats"><tr><td class="label">Operation</td><td class="label">Total</td></tr>',
                      '<tr><td class="label">Search</td><td class="content">%s</td></tr>' % len(search),
                      '<tr><td class="label">Browse</td><td class="content">%s</td></tr>' % len(browse),
                      '<tr><td class="label">Print</td><td class="content">%s</td></tr>' % len(printrecs),
                      '<tr><td class="label">Save</td><td class="content">%s</td></tr>' % len(save),
                      '<tr><td class="label">E-Mail</td><td class="content">%s</td></tr>' % len(email),
                      '</table>'])
        #end summary actions
        
        #query details
        indexes = {}
        relations = {}
        terms = {}
        operators = {}        
        queries = re.findall('QUERY:.*', allstring)
        total = len(queries)
        complex = 0
        for query in queries:
            query = query.replace('(', '').replace(')', '').replace('QUERY:', '')
            q = qf.get_query(session, query)
            lists = self._interpret(q, [[], [], [], []])
            if len(lists[3]) > 0:
                complex += 1
            for l in lists[0]:
                try:
                    indexes[l] += 1
                except:
                    indexes[l] = 1
            for l in lists[1]:
                try:
                    relations[l] += 1
                except:
                    relations[l] = 1            
            for l in lists[2]:
                try:
                    terms[l] += 1
                except:
                    terms[l] = 1              
            for l in lists[3]:
                try:
                    operators[l] += 1
                except:
                    operators[l] = 1   

        output.extend(['<table class="stats"><tr><td class="label">Query Type</td><td class="label">Total</td></tr>',
                       '<tr><td class="label">Total Single Clause Queries</td><td class="content">%d</td></tr>' % (total - complex),
                       '<tr><td class="label">Total Multiple Clause Queries</td><td class="content">%d</td></tr>' % complex,                       
                       '</table>' ])
     
        #operators
        output.append('<table class="stats"><tr><td class="label">Booleans</td><td class="label">Total</td></tr>')
        for k in ['and', 'or', 'not']:
            try:
                output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (k, operators[k]))
            except:
                output.append('<tr><td class="label">%s</td><td class="content">0</td></tr>' % (k))
        output.append('</table><br /></div><br />')    
                 
        #indexes
        output.append('<div class="statsdiv"><h3>Top 5s</h3><table class="stats"><tr><td class="label">Index</td><td class="label">Total</td></tr>')
        top5 = []
        for k in indexes.keys():
            top5.append([indexes[k], k])
        top5.sort(self.compare)
        for t in top5[:5]:     
            try:
                realIndex = idxNames[t[1]]
            except:
                realIndex = t[1]
            output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (realIndex, t[0]))
        output.append('</table>')         
        
        #terms 
        output.append('<table class="stats"><tr><td class="label">Terms</td><td class="label">Total</td></tr>')
        top5 = []
        for k in terms.keys():
            top5.append([terms[k], k])
        top5.sort(self.compare)
        for t in top5[:5]: 
            output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (t[1], t[0]))
        output.append('</table>')    
                
        #relations
        output.append('<table class="stats"><tr><td class="label">Type of Search</td><td class="label">Total</td></tr>')
        top5 = []
        for k in relations.keys():
            top5.append([relations[k], k])
        top5.sort(self.compare)
        for t in top5[:5]: 
            try:
                realRel = relationsMap[t[1]]
            except:
                realRel = t[1]
            output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (realRel, t[0]))
        output.append('</table><br /></div><br />')    
        
        #end query details
        
        if (file == 'searchhandler.log'):
            output.extend(['<form action="stats.html?operation=reset" method="post" onsubmit="return confirm(\'This operation will reset all statistics. The existing logfile will be moved and will be accessible from the drop down menu on the statistics page. Are you sure you want to continue?\');">',
                            '<p><input type="submit" name="resetstats" value=" Reset Statistics "/></p>',
                        '</form>'])
        
        return '<div id="maincontent">%s</div>' % ''.join(output)


    def compare(self, a, b):
        return cmp(int(b[0]), int(a[0])) # compare as integers


    def reset_statistics(self):
        newfilepath = os.path.join(statspath, 'searchhandler-%s.log' % (time.strftime('%Y-%m-%dT%H%M%S')))
        if not os.path.exists(searchlogfilepath): 
            self.logger.log('No logfile present at %s' % (searchlogfilepath))
            return 'No logfile present at specified location <code>%s</code>' % (searchlogfilepath)
        
        os.rename(searchlogfilepath, newfilepath)
        file(searchlogfilepath, 'w').close()
        self.logger.log('Search Statistics Reset')
        return 'Statistics reset. New logfile started. \n<br />\nOld logfiles can still be viewed by selecting them from the drop down box on the statistics page.\n<br />\n<br />\n<a href="menu.html" class="navlink">Back to \'Administration Menu\'</a>'
        #- end reset_statistics()
        

    def _interpret(self, what, output):
        if isinstance(what, Triple):
            self._interpret(what.leftOperand, output)
            try:
                bl = boolNames[what.boolean.value]
            except:
                bl = what.boolean.value
            output[3].append(bl)        
            if isinstance(what.rightOperand, Triple):
                self._interpret(what.rightOperand, output)
            else:
                self._interpret(what.rightOperand, output)       
            return output
        elif isinstance(what, SearchClause):
            try:
                idx = idxNames[what.index.value]
            except:
                idx = what.index.value
            output[0].append(idx)
            output[1].append(what.relation.value)
            for t in what.term.value.split():
                output[2].append(t)
            return output
        else:
            raise ValueError(what)
        
    
    def show_dataReqForm(self):
        menu = unicode(read_file('dataRequest.html'))
        return menu


    def get_libraryData(self, form, req):
        wstring = form.get('q', None)
        libraryfilter = form.get('libraryfilter', 'off')
        format = form.get('format', 'xml')
        outputfilter = form.get('filter', 'none').value
        xslt = etree.XSLT(etree.parse(os.path.join(dbPath, 'xsl', 'filterMarcFields.xsl')))
        params = {'locfilter': outputfilter}
        if wstring != None:
            words = wstring.split(';')
            anywords = []
            groups = []
            qString = []
            proxString = []
            for w in words:
                w = w.strip()
                wordset = w.split()
                if len(wordset) == 1:
                    anywords.append(w)
                else:
                    groups.append(w)
            if len(anywords):
                qString.append('c3.idx-kwd-location any "%s"' % ' '.join(anywords))
            if len(groups):                
                for group in groups:
                    group = group.split()
                    groupString = []
                    for word in group:
                        groupString.append('c3.idx-kwd-location all "%s"' % word)
                    proxString.append(''.join(['(', ' prox/unit=element/distance=0 '.join(groupString), ')']))
            if len(qString) and len(proxString):
                qString.append(' or ')
                qString.append(' or '.join(proxString))
            elif len(proxString):
                qString.append(' or '.join(proxString))                
            q = qf.get_query(session, ' '.join(qString))
            rs = db.search(session, q)
            if len(rs):
                if format == 'xml':
                    indentTxr = db.get_object(session, 'indentingTxr')
                    output = ['<?xml version="1.0" encoding="UTF-8"?>\n<collection>\n'] 
                    for r in rs :
                        newdoc = StringDocument(etree.tostring(xslt(r.fetch_record(session).get_dom(session), **params)))
                        newrec = xmlp.process_document(session, newdoc)
                        if libraryfilter == 'on':
                            newrec = self._filter_lib(newrec, wstring)
                        output.append(indentTxr.process_record(session, newrec).get_raw(session))
                    output.append('</collection>')
                    outpath = os.path.join(cheshirePath,
                                           'www',
                                           'istc',
                                           'output',
                                           'istc-marc21xml.xml'
                                           )
                    f = open(outpath, 'w')
                    f.write(''.join(output))
                    f.flush()
                    f.close()
                    req.headers_out["Content-Disposition"] = "attachment; filename=istc-marc21xml.xml"
                    req.content_type = "text/plain"
                    try:
                        req.sendfile(outpath)
                    except IOError, e:
                        req.content_type = "text/html"
                        req.write("Raised exception reads:\n<br>%s" % str(e))
                        return apache.OK
                    return apache.OK
                elif format == 'aleph':
                    marcAlephTxr = db.get_object(session, 'toTextTxr')
                    output = [] 
                    for r in rs :
                        rec = LxmlRecord(xslt(r.fetch_record(session).get_dom(session), **params))
                        if libraryfilter == 'on':
                            rec = self._filter_lib(rec, wstring)                        
                        output.append(marcAlephTxr.process_record(session, rec).get_raw(session))
                    outpath = os.path.join(cheshirePath,
                                           'www',
                                           'istc',
                                           'output',
                                           'istc-aleph.txt'
                                           )
                    f = open(outpath, 'w')
                    f.write('\n\n'.join(output))
                    f.flush()
                    f.close()
                    req.headers_out["Content-Disposition"] = "attachment; filename=istc-aleph.txt"
                    req.content_type = "text/plain"
                    try:
                        req.sendfile(outpath)
                    except IOError, e:
                        req.content_type = "text/html"
                        req.write("Raised exception reads:\n<br>%s" % str(e))
                        return apache.OK
                    return apache.OK
                elif format == 'exchange':
                    txr = db.get_object(session, 'toMarcTxr')
                    output = [] 
                    for r in rs :
                        rec = LxmlRecord(xslt(r.fetch_record(session).get_dom(session), **params))
                        if libraryfilter == 'on':
                            rec = self._filter_lib(rec, wstring)   
                        output.append(txr.process_record(session, rec).get_raw(session))
                    outpath = os.path.join(cheshirePath,
                                           'www',
                                           'istc',
                                           'output',
                                           'istc-exchange.txt'
                                           )
                    f = codecs.open(outpath, 'w', 'utf-8')
                    f.write(''.join(output))
                    f.flush()
                    f.close()
                    req.headers_out["Content-Disposition"] = "attachment; filename=istc-exchange.txt"
                    req.content_type = "text/plain"
                    try:
                        req.sendfile(outpath)
                    except IOError, e:
                        req.content_type = "text/html"
                        req.write("Raised exception reads:\n<br>%s" % str(e))
                        return apache.OK
                    return apache.OK
            else:
                content = self.show_dataReqForm()
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req) 
        else:
            content = self.show_dataReqForm()
            content = tmpl.replace('%CONTENT%', content)
            self.send_html(content, req)
        
    def _filter_lib(self, rec, wstring):
        words = wstring.split(';')
        tree = etree.fromstring(rec.get_xml(session))
        field9s = tree.xpath('//*[starts-with(@tag, "9")]/subfield[@code="a"]')
        parent = tree.xpath('//record')[0]
        for f in field9s:
            match = False
            for w in words:
                wordset = w.split()
                if len(wordset) == 1:
                    if f.text.find(wordset[0].strip()) != -1:
                        match = True
                elif len(wordset) == 0:
                    pass                
                else:
                    multiplematch = False
                    for word in wordset:
                        if f.text.find(word.strip()) != -1:
                            multiplematch = True
                        else:
                            multiplematch = False
                            break
                    if multiplematch == True:
                        match = True
            if match == False:
                parent.remove(f.xpath('parent::datafield')[0])
            
        doc = StringDocument(etree.tostring(tree))
        rec = xmlp.process_document(session, doc)
            
        return rec


    def print_searchResults(self, form):
        cql = self.generate_query(form)
        df = db.get_object(session, 'reportLabDocumentFactory')
        txr = db.get_object(session, 'printAllTxr')
        q = qf.get_query(session, cql.encode('utf-8'))
        rs = db.search(session, q)
        idx = db.get_object(session, 'idx-ISTCnumber')
        rs.order(session, idx, ascending=1, missing=[-1,1][1])
        if len(rs):
            for r in rs:
                record = r.fetch_record(session)
                doc = txr.process_record(session, record)
                string = doc.get_raw(session)               
                string = string.replace('%usalocs%', self.get_usaRefs(session, record))
                session.database = 'db_istc'
                doc = StringDocument(string)
                rec = xmlp.process_document(session, doc)
                df.load(session, rec)
            doc = df.get_document(session)
            return doc.get_raw(session)
        else:
            return self.show_adminMenu


    def print_alphaSelection(self, form):
        letters = form.get('alphabetchoice', None)
        output = []
        df = db.get_object(session, 'reportLabDocumentFactory')
        txr = db.get_object(session, 'printAllTxr')
        q = qf.get_query(session, 'c3.idx-ISTCnumber any %s*' % letters)
        rs = db.search(session, q)
        if len(rs):
            for r in rs:
                record = r.fetch_record(session)
                doc = txr.process_record(session, record)
                string = doc.get_raw(session)               
                string = string.replace('%usalocs%', self.get_usaRefs(session, record))
                session.database = 'db_istc'
                doc = StringDocument(string)
                rec = xmlp.process_document(session, doc)
                df.load(session, rec)
            doc = df.get_document(session)
            return doc.get_raw(session)
        else:
            return self.show_adminMenu
        

    def print_all(self, form):
        global recordStore
        output = []
        txr = db.get_object(session, 'printAllTxr')
        df = db.get_object(session, 'reportLabDocumentFactory')
        for record in recordStore:   
            doc = txr.process_record(session, record)
            string = doc.get_raw(session)               
            string = string.replace('%usalocs%', self.get_usaRefs(session, record))
            session.database = 'db_istc'
            doc = StringDocument(string)
            rec = xmlp.process_document(session, doc)
            df.load(session, rec)         
        doc = df.get_document(session)
        return doc.get_raw(session)



    def generate_query(self, form):
        self.logger.log('generating query')
        phraseRe = re.compile('".+?"')
        qClauses = []
        bools = []
        frombrowse = form.get('frombrowse', None)
        i = 1
        while (form.has_key('fieldcont%d' % i)):
            bools.append(form.getfirst('fieldbool%d' % (i-1), 'and'))
            i += 1
        i = 1

        while (form.has_key('fieldcont%d' % i)):
            cont = urllib.unquote(form.getfirst('fieldcont%d' % i)).decode('utf-8')
            idx = urllib.unquote(form.getfirst('fieldidx%d' % i, 'cql.anywhere')).decode('utf-8')
            rel = urllib.unquote(form.getfirst('fieldrel%d'  % i, 'all')).decode('utf-8')

            subClauses = []
            if (rel[:3] == 'all'): subBool = ' and '
            else: subBool = ' or '

            # in case they're trying to do phrase searching
            if (rel.find('exact') != -1 or rel.find('=') != -1 or rel.find('/string') != -1):
                # don't allow phrase searching for exact or /string searches
                cont = cont.replace('"', '\\"')
            else:
                phrases = phraseRe.findall(cont)
                for ph in phrases:
                    subClauses.append('(%s = %s)' % (idx, ph))

                cont = phraseRe.sub('', cont)
            if (idx and rel and cont):
                if idx == 'norzig.posessingInstitution' and not frombrowse:
                    subClauses.append(u'(%s %s "%s" or %s %s/usa "%s")' % (idx, rel, cont.strip(), idx, rel, cont.strip()))
                elif idx == 'istc.referencedBy' and not frombrowse:
                    subClauses.append(u'(%s %s "%s" or %s %s/full "%s")' % (idx, rel, cont.strip(), idx, rel, cont.strip()))
                else:
                    subClauses.append(u'%s %s "%s"' % (idx, rel, cont.strip()))

            if (len(subClauses)):
                qClauses.append('(%s)' % (subBool.join(subClauses)))

            # if there's another clause and a corresponding boolean
            try: qClauses.append(bools[i])
            except: break

            i += 1
            sys.stderr.write(repr(cont))
            sys.stderr.flush()

        qString = ' '.join(qClauses)
        self.logger.log('QUERY:' + qString)
        return qString


    def get_usaRefs(self, session, rec):
        session.database = dbusa.id
        usaRefs = []
        otherDict = {}
        qstring = []
        for node in rec.process_xpath(session, '//datafield[@tag="952"]'):
            ref = node.xpath('subfield[@code="a"]/text()')[0]
            other = node.xpath('subfield[@code="b"]/text()')
            if len(other):
                other = ' %s' % ' '.join(other)
            else:
                other = ''
            otherDict[ref] = other
            qstring.append('c3.idx-key-usa exact "%s"' % ref)
        if len(qstring) > 0:
            q = qf.get_query(session, ' or '.join(qstring))
            rs = dbusa.search(session, q)
            idx = dbusa.get_object(session, 'idx-location_usa')
            rs.order(session, idx)
            for r in rs:
                rec = r.fetch_record(session)
                usaRefs.append('%s%s' % (rec.process_xpath(session, '//full/text()')[0].strip(), otherDict[rec.process_xpath(session, '//code/text()')[0].strip()]))
            return externalDataTxr.process_record(session, xmlp.process_document(session, StringDocument('<string>%s</string>' % '; '.join(usaRefs).encode('utf-8').replace('&', '&amp;')))).get_raw(session).replace('&', '&amp;')
        else:
            return ''
        
        
# PDF Output functions ####################################################################



###########################################################################################




                  
    def handle(self, req):
        form = FieldStorage(req, True)  
                
        tmpl = unicode(read_file(self.baseTemplatePath))
        nav = unicode(read_file(self.editNavPath))
        tmpl = tmpl.replace('%NAVIGATION%', nav)
        
        path = req.uri[1:] 
        path = path[path.rfind('/')+1:]
        
        content = None      
        operation = form.get('operation', None)
        if path == 'database.html':
            if (operation) : 
                if (operation == 'rebuild'):
                    content = self.rebuild_database(form, req) 
                else:
                    content = self.show_adminMenu()
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
        elif path == 'pdf.html':
            if (operation):
                if (operation == 'allrecords'):
                    data = self.print_all(form)
                    self.send_pdf(data, req)
                    return
                elif (operation == 'alpha'):
                    data = self.print_alphaSelection(form)
                    self.send_pdf(data, req)
                    return    
                elif (operation == 'query'):
                    data = self.print_searchResults(form)
                    self.send_pdf(data, req)
                    return
                else:
                    content = unicode(read_file('pdfoutput.html'))
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
            else:
                content = unicode(read_file('pdfoutput.html'))
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
        elif path == 'users.html':
            if (operation) :              
                if (operation == 'adduser'):
                    content = self.add_user(form)
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
                elif (operation == 'delete'):
                    content = self.delete_user(form)
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
                elif (operation == 'edit'):
                    content = self.edit_user(form)
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)            
                else:
                    content = self.show_adminMenu()
                    content = tmpl.replace('%CONTENT%', content)
                    # send the display
                    self.send_html(content, req)
            else :  

                content = self.show_adminMenu()
                content = tmpl.replace('%CONTENT%', content)
                # send the display
                self.send_html(content, req)
        elif path == 'data.html':
            if (operation) :
                if (operation == 'library'):
                    self.get_libraryData(form, req)
                elif (operation == 'printall'):
                    content = self.printAll()
                    self.send_html(content, req)
                else:
                    content = self.show_dataReqForm()
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
            else:
                content = self.show_dataReqForm()
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)           
        elif path == 'stats.html':
            if (operation) :
                if operation == 'reset':
                    content = self.reset_statistics()
                    content = tmpl.replace('%CONTENT%', content)
                    self.send_html(content, req)
                else:
                   content = self.show_stats(form.get('file', 'searchhandler.log'))
                   content = tmpl.replace('%CONTENT%', content)
                   self.send_html(content, req) 
            else :
                content = self.show_stats(form.get('file', 'searchhandler.log'))
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
        else:
            if (operation == 'adduser'):
                content = self.add_user(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            else:
                content = self.show_adminMenu()
                content = tmpl.replace('%CONTENT%', content)
                # send the display
                self.send_html(content, req)
    
rebuild = True
serv = None
session = None
db = None
dbrefs = None
dbusa = None
qf = None
baseDocFac = None
sourceDir = None
editStore = None
recordStore = None
noteStore = None
userStore = None
authStore = None
xmlp = None
formTxr = None
indentingTxr = None
printAllTxr = None
externalDataTxr = None


def build_architecture(data=None):
    global rebuild, session, serv, db, dbPath, dbusa, dbrefs, qf, editStore, recordStore, usaRecordStore, \
    refsRecordStore, noteStore, authStore, userStore, xmlp, sourceDir, lockfilepath, reflockfilepath, usalockfilepath, \
    baseDocFac, usaDocFac, refsDocFac, buildSingleFlow, refsBuildSingleFlow, usaBuildSingleFlow, statspath, searchlogfilepath, \
    idxNames, relationsMap, printAllTxr, externalDataTxr
    
    if editStore:
        editStore.commit_storing(session)
    if noteStore:
        noteStore.commit_storing(session)
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
#    session.user = None
    serv = SimpleServer(session, os.path.join(cheshire3Root,
                                              'configs',
                                              'serverConfig.xml'))
    db = serv.get_object(session, 'db_istc')
    dbusa = serv.get_object(session, 'db_usa')
    dbrefs = serv.get_object(session, 'db_refs')
    dbPath = db.get_path(session, 'defaultPath')
    
    qf = db.get_object(session, 'baseQueryFactory')
    
    baseDocFac = db.get_object(session, 'istcDocumentFactory')
    usaDocFac = dbusa.get_object(session, 'usaDocumentFactory')
    refsDocFac = dbrefs.get_object(session, 'refsDocumentFactory')
    
    sourceDir = baseDocFac.get_default(session, 'data')
    
    editStore = db.get_object(session, 'editingStore')
    recordStore = db.get_object(session, 'recordStore')
    refsRecordStore = dbrefs.get_object(session, 'refsRecordStore')
    usaRecordStore = dbusa.get_object(session, 'usaRecordStore') 
    userStore = db.get_object(session, 'istcAuthStore')
    
    authStore = db.get_object(session, 'istcSuperAuthStore')
    xmlp = db.get_object(session, 'LxmlParser')
    buildSingleFlow = db.get_object(session, 'buildIndexSingleWorkflow'); buildSingleFlow.load_cache(session, db)
    refsBuildSingleFlow = dbrefs.get_object(session, 'refsBuildIndexSingleWorkflow'); refsBuildSingleFlow.load_cache(session, dbrefs)
    usaBuildSingleFlow = dbusa.get_object(session, 'usaBuildIndexSingleWorkflow'); usaBuildSingleFlow.load_cache(session, dbusa)
    
    printAllTxr = db.get_object(session, 'printAllTxr')
    externalDataTxr = db.get_object(session, 'externalDataTxr')
    
    rebuild = False
    
    idxNames = {"anywhere": 'General Keywords',
            "creator":'Author',
            "title":'Title',
            "originplace":'Location of Print',
            "countryofprint" : 'Country of Printing',
            "publisher":'Printer',
            "referencedby" : 'Bibliographical References',
            "identifier":'ISTC Number',
            "format":'Format',
            "posessinginstitution":'Location',
            "countryofcopy" : 'Country of Copy',
            "year":'Start or exact Year (008)',
            "date":'Publication Date',
            "language":'Language',
            "blshelfmark":'BL Shelfmark',
            "idx-pass-location_usa": 'USA Location',
            "idx-bibref": 'Bibliographical References',
                }
    
    relationsMap = {'all': 'All',
                    'any': 'Any',
                    '=' : 'Phrase',
                    '<' : 'Before',
                    '>' : 'After',
                    'exact' : 'Exactly'
                    }
    
    statspath = os.path.join(cheshirePath, 'www', 'istc', 'logs')
    searchlogfilepath = os.path.join(statspath, 'searchhandler.log')
    logfilepath = os.path.join(cheshirePath, 'www', 'istc', 'logs', 'adminhandler.log')
    lockfilepath = os.path.join(db.get_path(session, 'defaultPath'), 'indexing.lock')
    reflockfilepath = os.path.join(db.get_path(session, 'defaultPath'), 'refindexing.lock')
    usalockfilepath = os.path.join(db.get_path(session, 'defaultPath'), 'usaindexing.lock')


def handler(req):
    global rebuild, logfilepath, cheshirePath, db, editStore, xmlp, formTxr, script                # get the remote host's IP
    script = req.subprocess_env['SCRIPT_NAME']
    if (rebuild):
        build_architecture()
 #   req.register_cleanup(build_architecture)
    try:
        remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)
        # cd to where html fragments are
        os.chdir(os.path.join(cheshirePath, 'www', 'istc', 'html'))
        # Initialise logger object
        lgr = FileLogger(os.path.join(cheshirePath, 'www', 'istc', 'logs', '/adminhandler.log'), remote_host)
        # Initialise handler - with logger for this request
        istcAdminHandler = IstcAdminHandler(lgr)
        try:
            istcAdminHandler.handle(req)   
        finally:
            try:
                lgr.flush()
            except:
                pass
            del lgr, istcAdminHandler                                          # handle request
    except:
        req.content_type = "text/html"
        cgitb.Hook(file = req).handle()                                         # give error info
    else:
        return apache.OK


def authenhandler(req):
    global session, authStore, rebuild
    if (rebuild):
        build_architecture()
    pw = req.get_basic_auth_pw()
    un = req.user
    valid = check_password(un, pw)
    if valid is None:
        return apache.HTTP_UNAUTHORIZED
    elif valid:
        return apache.OK
    else:
        return apache.HTTP_UNAUTHORIZED
    #- end authenhandler()


def check_password(username, password):
    global session
    try:
        user = session.user = authStore.fetch_object(session, username)
    except:
        return None

    return (user and user.password == crypt(password, password[:2]))
