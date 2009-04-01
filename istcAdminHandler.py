#
# Script:    eadEditingHandler.py
# Version:   0.1
# Date:      ongoing
# Copyright: &copy; University of Liverpool 2008
# Description:
#            Data creation and editing interface for EAD finding aids
#            - part of Cheshire for Archives v3
#
# Author(s): CS - Catherine Smith <catherine.smith@liv.ac.uk>
#
# Language:  Python
# Required externals:
#            cheshire3-base, cheshire3-web
#            Py: 
#            HTML: 
#            CSS: 
#            Javascript: 
#            Images: 
#
# Version History: # left as example
# 0.01 - 06/12/2005 - JH - Basic administration navigations and menus

from mod_python import apache, Cookie
from mod_python.util import FieldStorage
import sys, os, cgitb, time, re, smtplib

sys.path.insert(1,'/home/cheshire/cheshire3/code')

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session
from cheshire3.utils import flattenTexts
from cheshire3.document import StringDocument
from cheshire3.record import Record
from cheshire3.record import LxmlRecord
from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.marc_utils import MARC
from cheshire3 import exceptions as c3errors
from cheshire3.cqlParser import parse, SearchClause, Triple
from lxml import etree
from copy import deepcopy
import datetime
#from wwwSearch import *
from crypt import crypt
from istcLocalConfig import *


class IstcAdminHandler:
    baseTemplatePath = cheshirePath + "/cheshire3/www/istc/html/baseTemplate.html"
    editNavPath = cheshirePath + "/cheshire3/www/istc/html/editNav.html"
    
    
    
    def __init__(self, lgr):
        self.logger = lgr

    def send_html(self, data, req, code=200):
        req.content_type = 'text/html; charset=utf-8'
        req.headers_out['Cache-Control'] = "no-cache, no-store"
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
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

        allstring = read_file('%s%s' % (statspath, file))
        output = []
        regex = re.compile('searchhandler\S')
        dateRegex = re.compile('[\S]*-(([\d]*)-([\d]*)-([\d]*))T([\d]{2})([\d]{2})([\d]{2}).log')
        
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
            output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (t[1], t[0]))
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
            output.append('<tr><td class="label">%s</td><td class="content">%s</td></tr>' % (t[1], t[0]))
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
        format = form.get('format', 'xml')
        if wstring != None:
            words = wstring.split()
            qString = []
            for w in words:
                qString.append('c3.idx-kwd-location all "%s"' % w)
            q = qf.get_query(session, ' prox/unit=element/distance=0 '.join(qString))
            rs = db.search(session, q)
            if len(rs):
                if format == 'xml':
                    output = [] 
                    for r in rs :
                        output.append(r.fetch_record(session).get_xml(session))
                    f = open(cheshirePath + '/cheshire3/www/istc/output/istc-marc21xml.xml', 'w')
                    f.write('\n\n'.join(output))
                    f.flush()
                    f.close()
                    req.headers_out["Content-Disposition"] = "attachment; filename=istc-marc21xml.xml"
                    req.content_type = "text/plain"
                    try:
                        req.sendfile('/home/cheshire/cheshire3/www/istc/output/istc-marc21xml.xml')
                    except IOError, e:
                        req.content_type = "text/html"
                        req.write("Raised exception reads:\n<br>%s" % str(e))
                        return apache.OK
                    return apache.OK
                elif format == 'aleph':
                    marcAlephTxr = db.get_object(session, 'toTextTxr')
                    output = [] 
                    for r in rs :
                        output.append(marcAlephTxr.process_record(session, r.fetch_record(session)).get_raw(session))
                    f = open(cheshirePath + '/cheshire3/www/istc/output/istc-aleph.txt', 'w')
                    f.write('\n\n'.join(output))
                    f.flush()
                    f.close()
                    req.headers_out["Content-Disposition"] = "attachment; filename=istc-aleph.txt"
                    req.content_type = "text/plain"
                    try:
                        req.sendfile('/home/cheshire/cheshire3/www/istc/output/istc-aleph.txt')
                    except IOError, e:
                        req.content_type = "text/html"
                        req.write("Raised exception reads:\n<br>%s" % str(e))
                        return apache.OK
                    return apache.OK
                elif format == 'exchange':
                    pass                       
        else:
            content = self.show_dataReqForm()
            content = tmpl.replace('%CONTENT%', content)
            self.send_html(content, req)
        
                       
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
authStore = None
xmlp = None
formTxr = None
indentingTxr = None


def build_architecture(data=None):
    global rebuild, session, serv, db, dbPath, dbusa, dbrefs, qf, editStore, recordStore, usaRecordStore, \
    refsRecordStore, noteStore, authStore, userStore, xmlp, sourceDir, lockfilepath, reflockfilepath, usalockfilepath, \
    baseDocFac, usaDocFac, refsDocFac, buildSingleFlow, refsBuildSingleFlow, usaBuildSingleFlow, statspath, searchlogfilepath
    
    if editStore:
        editStore.commit_storing(session)
    if noteStore:
        noteStore.commit_storing(session)
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
#    session.user = None
    serv = SimpleServer(session, cheshirePath + '/cheshire3/configs/serverConfig.xml')
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
    
    
    rebuild = False
    
    
    statspath = cheshirePath + '/cheshire3/www/istc/logs/'
    searchlogfilepath = statspath + 'searchhandler.log'
    logfilepath = cheshirePath + '/cheshire3/www/istc/logs/edithandler.log'
    lockfilepath = db.get_path(session, 'defaultPath') + '/indexing.lock'
    reflockfilepath = db.get_path(session, 'defaultPath') + '/refindexing.lock'
    usalockfilepath = db.get_path(session, 'defaultPath') + '/usaindexing.lock'


def handler(req):
    global rebuild, logfilepath, cheshirePath, db, editStore, xmlp, formTxr, script                # get the remote host's IP
    script = req.subprocess_env['SCRIPT_NAME']
 #   req.register_cleanup(build_architecture)
    try :
        remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)
        os.chdir(os.path.join(cheshirePath, 'cheshire3', 'www', 'istc', 'html'))     # cd to where html fragments are
        lgr = FileLogger(cheshirePath + '/cheshire3/www/istc/logs/adminhandler.log', remote_host)                                  # initialise logger object
        istcAdminHandler = IstcAdminHandler(lgr)                                      # initialise handler - with logger for this request
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
    else :
        return apache.OK



def authenhandler(req):
    global session, authStore, rebuild
    if (rebuild):
        build_architecture()                                                    # build the architecture
    pw = req.get_basic_auth_pw()
    un = req.user
    try: session.user = authStore.fetch_object(session, un)
    except: return apache.HTTP_UNAUTHORIZED    
    if (session.user and session.user.password == crypt(pw, pw[:2])):
        return apache.OK
    else:
        return apache.HTTP_UNAUTHORIZED
    #- end authenhandler()