#
# Script:    istcEditingHandler.py
# Version:   0.1
# Date:      ongoing
# Copyright: &copy; University of Liverpool 2009
# Description:
#           Editing/Creation Interface for ISTC
#
# Author(s): CS - Catherine Smith <catherine.smith@liv.ac.uk>
#
# Language:  Python
#
# Version History: 
# 0.01 - 25/06/2009 - CS - Everything needed for inital release


from mod_python import apache, Cookie
from mod_python.util import FieldStorage
import sys, os, cgitb, time, re, smtplib

sys.path.insert(1,'/home/cheshire/cheshire3/code')

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session
from cheshire3.utils import flattenTexts
from cheshire3.document import StringDocument
from cheshire3.record import LxmlRecord
from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.marc_utils import MARC
from cheshire3 import exceptions as c3errors
from lxml import etree
from copy import deepcopy
import datetime
#from wwwSearch import *
from crypt import crypt
from istcLocalConfig import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class IstcEditingHandler:
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


    def send_xml(self, data, req, code=200):
        req.content_type = 'text/xml'
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        try:
            data = data.encode('utf-8')
        except:
            pass
        req.write(data)
        req.flush()       
    #- end send_xml()

#########################################################################################
# User Editing
#
    def edit_user(self, form):
        global authStore, rebuild
        userid = form.get('userid', session.user.id)
        try:
            user = authStore.fetch_object(session, userid)
        except:
            return '<p>User with id "%s" does not exist!</p><a href="menu.html">Return to \'Main Menu\'.<a/>' % (userid)

        if (form.get('submit', None)):
            userRec = authStore.fetch_record(session, userid)
            userNode = userRec.get_dom(session)
            passwd = form.get('passwd', None)
            # check password
            if (passwd and user.check_password(session, passwd)):
                newHash = {}
                for f in user.simpleNodes:
                    if form.has_key(f):
                        newHash[f] = form.getfirst(f)
                passwd1 = form.get('passwd1', None)
                if (passwd1 and passwd1 != ''):
                    passwd2 = form.get('passwd2', None)
                    if (passwd1 == passwd2):
                        newHash['password'] = crypt(passwd1, passwd1[:2])
                    else:
                        content = '<span class="userediterror">Unable to update details - new passwords did not match. Please try again.</span> %s' % read_file('editusermenu.html')                       
                        replaceHash = {
                           '%USERNAME%' : session.user.username,
                           '%realName%': session.user.realName,
                           '%email%' : session.user.email,
                           '%tel%' : session.user.tel                       
                           }       
                        return multiReplace(content, replaceHash) 
                
                # update DOM
                userNode = self._modify_userLxml(userNode, newHash)    
                self._submit_userLxml(userid, userNode)                    
                user = authStore.fetch_object(session, userid)
                rebuild = True                   
                return '<div id="maincontent"><h1>Details successfully updated</h1><a href="menu.html">Return to \'Main Menu\'.<a/>'
            else:
                content = '<span class="userediterror">Unable to update details - current password missing or incorrect. Please try again.</span> %s' % read_file('editusermenu.html')                        
                replaceHash = {
                   '%USERNAME%' : session.user.username,
                   '%realName%': session.user.realName,
                   '%email%' : session.user.email,
                   '%tel%' : session.user.tel                       
                   }       
                return multiReplace(content, replaceHash)               
        form = read_file('edituser.html').replace('%USERNAME%', userid)
        for f in user.simpleNodes:
            if hasattr(user,f): form = form.replace('%%%s%%' % f, getattr(user,f))
            else: form = form.replace('%%%s%%' % f, '')
        return form
        #- end edit_user()


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
        authStore.store_record(session, rec)
        authStore.commit_storing(session)
        #- end _submit_userLxml()


    def build_marc(self, form, date=None):
        self.logger.log('building marc')
        multipleEntryFields = ['imprints', 'generalnotes', 'references', 'repnotes', 'holdings', 'blshelfmarks']
        list = form.list
        dict = {}
        marc = {}

        for l in list:
            if l.value.strip() != '' and l.value.strip() != ' ' and l.name not in ['operation']:
                if l.name == '1':
                    marc[1] = [l.value.strip()]
                elif l.name == 'leader':
                    try:
                        marc[0] = [''.join([l.value[5:9], l.value[17:20]])]
                    except:
                        marc[0] = [' am    ']
                elif l.name in multipleEntryFields or l.name[3:] in multipleEntryFields:
                    if l.name == 'references':
                        if l.value.find('|||') != -1:
                            meList = l.value.split('|||')
                            ind = '0-0'
                            codelist = []
                            a = ''
                            other = ''
                            for me in meList:
                                if me.strip() != '': 
                                    temp = me.split('|')
                                    code = temp[0].split('_')[1].strip()
                                    if code == 'ind':
                                        n = int(temp[0].split('_')[0])
                                        ind = temp[1]
                                    elif code == 'a':
                                        a = temp[1].strip()
                                    elif code == 'other':
                                        other = temp[1].strip()
                            tuple = ((ind.split('-')[0].strip(), ind.split('-')[1].strip(), [('a', '%s %s' % (a, other)) ]))
                            try:
                                marc[n].append(tuple)
                            except:
                                marc[n] = [tuple]
                    else:
                        if l.value.find('|||') != -1:
                            meList = l.value.split('|||')
                            ind = '0-0'
                            codelist = []
                            for me in meList:  
                                self.logger.log(me)
                                if me.strip() != '': 
                                    temp = me.split('|')
                                    code = temp[0].split('_')[1].strip()
                                    if code == 'ind':
                                        try:
                                            n = int(temp[0].split('_')[0])
                                        except:
                                            pass
                                        ind = temp[1]
                                    elif code == 'country':
                                        n = int(temp[1])
                                    else:
                                        codelist.append((code, temp[1].strip()))
                                        self.logger.log(codelist)
                            tuple = ((ind.split('-')[0].strip(), ind.split('-')[1].strip(), codelist))
                            try:
                                marc[n].append(tuple)
                            except:
                                marc[n] = [tuple]
                else:
                    name = l.name.split('_')
                    if len(name) > 1:
                        try:
                            n = int(name[0])
                        except:
                            n = name[0]
                        try:
                            dict[n][name[1]] = l.value.strip()
                        except:                   
                            dict[n] = {name[1] : l.value.strip()}   
        try:
            marc[0]
        except:
            marc[0] = [' am    '] 
        
        authorTag = dict['author']['sel']
        if not authorTag == 'null':
            authorTag = int(authorTag)
            dict[authorTag] = dict['author']
            del dict[authorTag]['sel']
        del dict['author']

        for k in dict.keys():
            if k == 8:
                try:
                    orig = dict[8]['original']
                except:
                    orig = '      '
                try:
                    dateType = dict[8]['datetype']
                except:
                    dateType = ' '
                try:
                    date1 = dict[8]['date1']
                except:
                    date1 = '    '
                try:
                    date2 = dict[8]['date2']
                except:
                    date2 = '    '          
                try:
                    lang = dict[8]['lang']      
                except:
                    lang = '   '
                string = '%s%s%s%s                    %s  ' % (orig, dateType, date1, date2, lang)
                marc[8] = [string]

            elif len(dict[k]) > 1:
                inds = ['0', '0']
                list = []
                marc[k] = []
                for y in dict[k].keys():              
                    if y == 'ind':
                        inds = dict[k]['ind'].split('-')
                    else :
                        list.append((y, dict[k][y]))                    
                marc[k].append((inds[0], inds[1], list)) 
        if date != None:
            marc[959] = [('0', '0', [('a', '%s-%s' % (time.strftime('%Y%m%d'), session.user.username))])]
        marcObject = MARC()
        self.logger.log(marc)
        marcObject.fields = marc           
        return marcObject.toMARCXML()

 
    def get_fullRefs(self, session, form, recursive=True):
        ref = form.get('q', None)
        ref = ref.replace('*', '\*')
        ref = ref.replace('?', '\?')  
        ref = ref.replace('"', '\\"')      
        r = form.get('r', '') 
        if r != '':
            recursive=False
        session.database = dbrefs.id
        q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (ref))
        rs = dbrefs.search(session, q)
        if len(rs):
            recRefs = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
        else :
            if recursive :
                while ref.rfind(' ') != -1 and not len(rs):
                    ref = ref[:ref.rfind(' ')].strip()
                    q.term.value = ref.decode('utf-8')
                    rs = dbrefs.search(session, q)
                if len(rs):
                    recRefs = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
                else:
                    recRefs = '' 
            else:
                recRefs = '' 
        return recRefs


    def get_fullUsa(self, session, form):
        code = form.get('q', None)
        code = code.replace('*', '\*')
        code = code.replace('?', '\?')        

        session.database = dbusa.id
        q = qf.get_query(session, 'c3.idx-key-usa exact "%s"' % (code))
        rs = dbusa.search(session, q)
        if len(rs):
            fullUsa = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
        else :
           fullUsa = '' 
        return fullUsa
       
        
    def _walk_directory(self, d, type='checkbox'):
        # we want to keep all dirs at the top, followed by all files
        outD = []
        outF = []
        filelist = os.listdir(d)
        filelist.sort()
        for f in filelist:
            if (os.path.isdir(os.path.join(d,f))):
                outD.extend(['<li title="%s">%s' % (os.path.join(d,f),f),
                            '<ul class="hierarchy">',
                            '\n'.join(self._walk_directory(os.path.join(d, f), type)),
                            '</ul></li>'
                            ])
            else:
                fp = os.path.join(d,f)
                outF.extend(['<li>'
                            ,'<span class="fileops"><input type="%s" name="filepath" value="%s"/></span>' % (type, fp)
                            ,'<span class="filename">%s</span>' % (f)
                            ,'</li>'
                            ])

        return outD + outF
        
        #- end walk_directory()
    
    
    def _walk_store(self, storeName, type='checkbox', userStore=None):
        store = db.get_object(session, storeName)
        if not userStore:
            out = []
            for s in store :
                out.extend(['<li class="unmarked>'
                           ,'<span class="fileops"><input type="%s" name="recid" value="%s"/></span>' % (type, s.id)
                           ,'<span class="filename">%s</span>' % s.id[:s.id.rfind('-')]
                           ,'</li>'
                           ])
            return out
        else :
            out = []
            names = []
            userStore = db.get_object(session, userStore)
            total = 0;
            for user in userStore :
                name = user.username
                names.append(name)
                if name == session.user.username or session.user.has_flag(session, 'info:srw/operation/1/create', 'eadAuthStore'):
                    disabled = ''
                else :
                    disabled = 'disabled="disabled"'
                userFiles = ['<li title=%s class="unmarked"><span>%s</span>' % (name, name), '<ul class="hierarchy">'] 
                for s in store:
                    if s.id[s.id.rfind('-')+1:] == name:
                        userFiles.extend(['<li class="unmarked">'
                                           ,'<span class="fileops"><input type="%s" name="recid" value="%s" %s/></span>' % (type, s.id, disabled)
                                           ,'<span class="filename">%s</span>' % s.id[:s.id.rfind('-')]
                                           ,'</li>'
                                           ])
                        total += 1;
                userFiles.append('</ul></li>')
                out.append(''.join(userFiles))

            if session.user.has_flag(session, 'info:srw/operation/1/create', 'eadAuthStore'):
                disabled = ''
            else :
                disabled = 'disabled="disabled"'
            for s in store:
                if s.id[s.id.rfind('-')+1:] not in names:
                    out.extend(['<li title=deletedUsers><span>Deleted Users</span>', '<ul class="hierarchy">', '<li>'
                                               ,'<span class="fileops"><input type="%s" name="recid" value="%s" %s/></span>' % (type, s.id, disabled)
                                               ,'<span class="filename">%s</span>' % s.id[:s.id.rfind('-')]
                                               ,'</li>'])
            return out



 
 
#########################################################################################
# Loading into Interface
#            
       
    def generate_file(self, form):
        page = unicode(read_file('editExtras.html'))

        doc = StringDocument('<record></record>')         
        rec = xmlp.process_document(session, doc)
        content = unicode(formTxr.process_record(session, rec).get_raw(session))
        content = content.replace('%%INTERNALNOTES%%', u' ')            
        page = page.replace('%CONTENT%', content)
        page = page.replace('%OWNER%', session.user.username)
        page = page.replace('%%timestamp%%', u' ')
        return page      
        
     
    #from editing store 
    def load_file(self, form):   
        recid = form.get('recid', None)
        if recid == None:
            return 'no recid'
        
        if recid.rfind('-') != -1:
            owner = recid[recid.rfind('-')+1:]
            recid = recid[:recid.rfind('-')]
        else :
            owner = session.user.username
                         
        rec = editStore.fetch_record(session, '%s-%s' % (recid, owner))
        try:
            notes = noteStore.fetch_document(session, recid).get_raw(session)
        except:
            notes = ' '
        
        page = unicode(read_file('editExtras.html'))
        content = unicode(formTxr.process_record(session, rec).get_raw(session))
        
        content = content.replace('%RFRNC%', self._get_refxml(session, rec))
        content = content.replace('%OWNER%', owner)
        content = content.replace('%%INTERNALNOTES%%', notes)      
        page = page.replace('%CONTENT%', content)
        page = page.replace('%%timestamp%%', unicode(self._get_timeStamp()))
        return page

  
                   
    #from file
    def edit_file(self, form):
        
        f = form.get('q', None)
        
        if f == None:
            f = form.get('filename', None)            
            if f == None:
                return '<p>No files selected</p>'           
        if (f.find('.xml') == -1):
            f = '%s.xml' % f
        
        xml = read_file('%s/%s' % (sourceDir, f))

        doc = StringDocument(xml)  
        rec = xmlp.process_document(session, doc)
        
        # TODO: handle file not successfully parsed
        if not isinstance(rec, LxmlRecord):
            return rec     
        istcNo = rec.process_xpath(session, '//controlfield[@tag="001"]/text()')[0]        
        recid = '%s-%s' % (istcNo, session.user.username)
        rec.id = recid
        try:
            rec = editStore.fetch_record(session, recid)
        except:
            editStore.store_record(session, rec)
        editStore.commit_storing(session) 
        try:
            notes = noteStore.fetch_document(session, istcNo).get_raw(session)
        except:
            notes = ' '
               
        page = unicode(read_file('editExtras.html'))
        content = unicode(formTxr.process_record(session, rec).get_raw(session))
        
        content = content.replace('%RFRNC%', self._get_refxml(session, rec))
        content = content.replace('%OWNER%', session.user.username)
        content = content.replace('%%INTERNALNOTES%%', notes)      
        page = page.replace('%CONTENT%', content)
        page = page.replace('%%timestamp%%', unicode(self._get_timeStamp()))
        return page

####################################################################################################



    def _get_refxml(self, session, rec):
        bibRefNormalizer = db.get_object(session, 'BibRefNormalizer')
        f510 = rec.process_xpath(session, '//datafield[@tag ="510"]/subfield/text()')
        if not len(f510):
            return '<div id="addedreferences" style="display:none" class="added" onmouseout="getFormRef()"><ul id="addedreferenceslist"></ul></div>'
        else:
            output = []
            for index, t in enumerate(f510):
                t = unicode(t)
                abbrev = bibRefNormalizer.process_string(session, t)
                self.logger.log('------------------------------------%s------------------------------' % abbrev)
                other = t[len(abbrev) + 1:]
                session.database = dbrefs.id
                q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (abbrev.replace('*', '\*').replace('?', '\?').replace('"', '\\"')))
                rs = dbrefs.search(session, q)
                if len(rs):
                    full =  rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
                else:
                    full = abbrev
                hidden = '510_a | %s ||| 510_other | %s ||| 510_ind | 4-0 ||| ' % (abbrev.replace('"', '&quot;'), other)

                output.extend([u'<li style="position: relative;" id="lireferences_formgen%d">' % index ,
                               u'<div id="references_formgen%d">' % index,
                               u'<div class="icons"><a onclick="deleteEntry(\'references_formgen%d\');" title="delete entry">' % index,
                               u'<img class="addedimage" src = "/istc/images/remove.png" onmouseover="this.src=\'/istc/images/remove-hover.png\';" onmouseout="this.src=\'/istc/images/remove.png\';" id="delete_formgen%d" /></a>' % index,
                               u'<a onclick="entryUp(\'references_formgen%d\');" title="move up">' % index,
                               u'<img class="addedimage" src = "/istc/images/up.png" onmouseover="this.src=\'/istc/images/up-hover.png\';" onmouseout="this.src=\'/istc/images/up.png\';" id="up_formgen%d"/></a>' % index,
                               u'<a onclick="entryDown(\'references_formgen%d\');" title="move down">' % index,
                               u'<img class="addedimage" src = "/istc/images/down.png" onmouseover="this.src=\'/istc/images/down-hover.png\';" onmouseout="this.src=\'/istc/images/down.png\';" id="down_formgen%d"/></a>' % index,                                               
                               u'<a onclick="insertAbove(\'references_formgen\', %d);" title="insert above">' % index,
                               u'<img class="addedimage" src = "/istc/images/insert.png" onmouseover="this.src=\'/istc/images/insert-hover.png\';" onmouseout="this.src=\'/istc/images/insert.png\';" id="insert_formgen%d"/></a>' % index,                                               
                               u'</div>',
                               u'<div class="multipleEntry">',
                               u'<p class="addedString" title="%s"><a onclick="editEntry(\'references_formgen\', %d);">' % (full, index), 
                               u'%s %s' % (abbrev, other),
                               u'</a></p></div></div>',
                               u'<input id="references_formgen%dxml" name="references" value="%s" type="hidden" />' % (index, hidden),
                               u'</li>'])
            return u'<div style="display: block;" class="added" id="addedreferences"><ul id="addedreferenceslist">%s</ul></div>' % ''.join(output)
          
           
    def show_editMenu(self, type):
        global sourceDir
        self.logger.log('Create/Edit Options')

        if type == 'edit':
            page = read_file('editsubmenu.html')
            recids = self._walk_store('editingStore', 'radio', 'istcAuthStore') 
            page = page.replace('%%%RECORDS%%%', ''.join(recids))
            session.database = db.id
            q = qf.get_query(session, 'c3.idx-location-private all "Private"')
            rs = db.search(session, q)
            private = []
            if len(rs):
                private.append('<form action="edit.html" method="get" enctype="multipart/form-data" onsubmit="return checkIds(\'private\');"><input type="hidden" name="operation" id="operation2" value="edit"/><ul class="unmarked">')
                for r in rs:
                    istcNo = r.fetch_record(session).process_xpath(session, '//controlfield[@tag="001"]/text()')[0]
                    private.extend(['<li class="unmarked">'
                                    ,'<span class="fileops"><input type="radio" name="q" value="%s"/></span>' % istcNo
                                    ,'<span class="filename">%s</span>' % istcNo
                                    ,'</li>'
                                  ])
                private.append('</ul><input class="editbutton" type="submit" value=" Edit File "/></form><br/>')
            else:
                private.append('no records have private data') 
                
            page = page.replace('%%%PRIVATE%%%', ' '.join(private))
            

        elif type == 'main':
            page = read_file('editmenu.html')
                
                     
        elif type == 'user':
            page = read_file('editusermenu.html')
            replaceHash = {
                           '%USERNAME%' : session.user.username,
                           '%realName%': session.user.realName,
                           '%email%' : session.user.email,
                           '%tel%' : session.user.tel                       
                           }       
            page = multiReplace(page, replaceHash)    
        
        elif type == 'delete':
            page = read_file('deletesubmenu.html')
        elif type == 'editref':
            page = read_file('editref.html')
        elif type == 'editusa':
            page = read_file('editusa.html')     
        return page
 
 
    def _cleverTitleCase(self, txt):
        words = txt.split()
        for x in range(len(words)):
            if (x == 0 and not words[x][0].isdigit()) or (words[x][0].isalpha()) and (words[x] not in ['de']):
                words[x] = words[x].title()
        return ' '.join(words)


    def delete_file(self, req, form):
        operation = form.get('operation', 'unindex')
        self.logger.log(operation)
        if (operation.strip() == 'Delete + Unindex'):
            operation = 'unindex'      
        else:
            operation = 'delete'
        filepaths = form.getlist('filename')
        # setup http headers etc
        req.content_type = 'text/html'
        req.send_http_header()
        head = unicode(read_file('header.html'))
        nav = unicode(read_file('editNav.html'))
        req.write(head)     
        req.write(nav)
        req.write('<div id="maincontent">')
        if (len(filepaths) == 0):
            return '%s<br />\n<br/><a href="menu.html" title="Main Menu" class="navlink">Back to \'Main Menu\'</a>.' % self.review_records(operation)     
        if os.path.exists(lockfilepath):
            req.write('<p><span class="error">[ERROR]</span> - Another user is already indexing this database so no files can currently be deleted or unindexed. Please try again in 10 minutes.</p>\n<p><a href="menu.html">Back to \'Main Menu\'</a>.</p>')
        else :  
            lock = open(lockfilepath, 'w')
            lock.close() 
            try:
                deletedTotal = 0
                unindexedTotal = 0
                errorTotal = 0
                for i, filepath in enumerate(filepaths):
                    if filepath.find('.xml') == -1:
                        filepath = '%s.xml' % filepath
                    filepath = '%s/%s' % (sourceDir, filepath)
                    if not filepath:
                        return '<span class="error">[ERROR]</span> - Could not locate specified file path %s' % filepath     
                    try:
                        os.remove(filepath)
                        req.write('<span class="ok">[OK]</span><br/>\n')
                        deletedTotal += 1;
                        self.logger.log('File Delete: %s removed from disk' % (filepath))
                    except:
                        req.write('<span class="error">[ERROR]</span> - Could not delete file from disk<br/>')
                                                           
                    if (operation == 'unindex'):
                        req.write('Processing...')
                        recid = filepath[filepath.rfind('/')+1:-4]
                        req.write('<br/>\nUnindexing record: %s ...' % recid)
                        try:
                            rec = recordStore.fetch_record(session, recid)
                        except (c3errors.FileDoesNotExistException, c3errors.ObjectDoesNotExistException):
                            # hmm record doesn't exist, simply remove file from disk (already done!)
                            req.write('<span class="error">[ERROR]</span> - Record not present in recordStore<br/>\n')
                            errorTotal += 1
                        else:
                            # delete from indexes
                            db.unindex_record(session, rec)
                            db.remove_record(session, rec)
                            req.write('<span class="ok">[OK]</span><br/>\nDeleting record from stores ...')
                            # delete from recordStore
                            recordStore.begin_storing(session)
                            recordStore.delete_record(session, rec.id)
                            recordStore.commit_storing(session)

                            req.write('<span class="ok">[OK]</span><br/>\n')
                            
                        req.write('Merging modified indexes...')
                        try:
                            db.commit_indexing(session)
                        except c3errors.FileDoesNotExistException:
                            # FIXME: R to investigate Cheshire3 quirk
                            req.write('<span class="ok">[OK]</span><br/>\n')
                            unindexedTotal += 1
                        except:
                            req.write('<span class="ok">[INCOMPLETE]</span> - File may still be available until the database is rebuilt.<br/>\n')
                            unindexTotal +=1
                            errorTotal += 1
                        else:
                            db.commit_metadata(session)
                            req.write('<span class="ok">[OK]</span><br/>\n')
                            unindexedTotal += 1
                        self.logger.log('File Delete: %s removed from database' % (recid))
                        rebuild = True
                        
                if (operation == 'unindex'):
                    req.write('\n<strong>%d file(s) unindexed and deleted</strong>' % unindexedTotal)
                else :
                    req.write('\n<strong>%d file(s) deleted</strong>' % deletedTotal)
                    req.write('\n<p>Files will remain in the database until the database is rebuilt.</p>')
                if (errorTotal > 0):
                    req.write('\n<strong> with %d possible error(s) (see above for details)</strong>' %errorTotal)
                req.write('\n<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')
                
            finally:
                if os.path.exists(lockfilepath):
                    os.remove(lockfilepath)    
        foot = unicode(read_file('footer.html'))
        req.write('</div>')      
        req.write(foot)
        return None
    #- end delete_file()
             
 
#########################################################################################
# Functions
#

#    def file(self, form):
#        self.logger.log('submitting to file')
#        recid = form.get('1', None)
#        owner = form.get('owner', session.user.username)
#        recid = '%s-%s' % (recid, owner)
#        rec = editStore.fetch_record(session, recid)
#        df = db.get_object(session, 'istcDocumentFactory')
#        sourceDir = df.get_default(session, 'data')
#        filename = '%s.xml' % recid
#        filepath = os.path.join(sourceDir, filename)
#        if os.path.exists(filepath):
#            os.remove(filepath)
#        try :
#            file = open(filepath, 'w')
#        except :
#            pass # put sensible error in 
#        indentTxr = db.get_object(session, 'indentingTxr')
#        file.write(indentTxr.process_record(session, tempRec).get_raw(session))
#        file.flush()
#        file.close()    
#        editStore.delete_record(session, recid)
#        editStore.commit_storing(session)
#        
#        
#    def index(self, form):    
#        self.logger.log('indexing')
#        recid = form.get('1', None)
#        rec = editStore.fetch_record(session, recid)        
#        
#        
    def save(self, form):
        self.logger.log('saving form')
        recid = form.get('1', None)
        owner = form.get('owner', session.user.username)
        rec = xmlp.process_document(session, StringDocument(self.build_marc(form)))
        rec.id = '%s-%s' % (recid, owner)
        editStore.store_record(session, rec)
        editStore.commit_storing(session)
        
        notes = StringDocument(form.get('internal_notes', None))
        notes.id = recid
        noteStore.store_document(session, notes)        
        noteStore.commit_storing(session)     
        self.logger.log('form saved at %s' % self._get_timeStamp())
        return self._get_timeStamp()


    def delete(self, form):
        recid = form.get('1', None)
        if (recid == None):
            recid = form.get('recid', None)
        if (recid.find('-') == -1):
            owner = form.get('owner', session.user.username)
            recid = '%s-%s' % (recid, owner)   
        editStore.delete_record(session, recid)
        editStore.commit_storing(session)
        return self.show_editMenu('edit')
        
        
    def preview_xml(self, form):
        recid = form.get('1', None)
        owner = form.get('owner', session.user.username)
        recid = '%s-%s' % (recid, owner)
        rec = editStore.fetch_record(session, recid)  
        return rec.get_xml(session)

    
    def preview_marc(self, form):
        marcAlephTxr = db.get_object(session, 'toAleph')
        recid = form.get('1', None)
        owner = form.get('owner', session.user.username)
        recid = '%s-%s' % (recid, owner)
        rec = editStore.fetch_record(session, recid)        
        return u'<div id="maincontent"><h1>Marc Preview</h1>%s</div>' % unicode(marcAlephTxr.process_record(session, rec).get_raw(session))


    def email(self, form):
        recid = form.get('1', None)
        owner = form.get('owner', session.user.username)
        recid = '%s-%s' % (recid, owner)
        rec = editStore.fetch_record(session, recid)  
        email = session.user.email
        marcTextTxr = db.get_object(session, 'toTextTxr')
        message = MIMEMultipart()
        message['From'] = 'john.goldfinch@bl.uk'
        message['To'] = email
        message['Subject'] = 'ISTC Record'
        message.attach(MIMEText(marcTextTxr.process_record(session, rec).get_raw(session)))
        
        smtp = smtplib.SMTP()
        smtp.connect(host='mail1.liv.ac.uk', port=25)
        smtp.sendmail('cheshire@liv.ac.uk', email, message.as_string())
        smtp.close()
        return ('<div id="maincontent"><h1>File Emailed</h1><p>The record you requested was emailed to %s</p></div>' % email)


 
    def _get_timeStamp(self):
        return time.strftime('%H:%M') 
 
##########################################################################################
# AJAX calls 
#

    def _get_suggestions(self, form):
        letters = form.get('s', None)
        index = form.get('i', None)
        if index == 'idx-key-refs-exact':
            session.db = dbrefs.id
            q = qf.get_query(session, 'c3.%s = "%s"' % (index, letters))
            terms = dbrefs.scan(session, q, 50, direction="=")   
        elif index == 'idx-key-usa':
            session.db = dbusa.id
            q = qf.get_query(session, 'c3.%s = "%s"' % (index, letters))
            terms = dbusa.scan(session, q, 50, direction="=")                        
        else:
            q = qf.get_query(session, 'c3.%s = "%s"' % (index, letters))
            terms = db.scan(session, q, 50, direction="=")
        output = []
        for t in terms:
            term = t[0]
            output.append('%s (%i)' % (term, t[1][1]))
            #TODO: check that t[1][1] is actually no of occs not no of recs (may need to be t[1][2])
        if len(output):
            return '<select>%s</select>' % ' | '.join(output)
        else:
            return '<select></select>'    
        
        
    def _get_all(self, form):
        letters = form.get('letters', None)
        type = form.get('type', 'checkbox')
        files = os.listdir(sourceDir)
        
        output = []
        for f in files:
            if f.find(letters) == 0:
                output.append('<input type="%s" name="filename" value="%s"/>%s<br/>' % (type, f[:-4], f[:-4]))
        output.sort()
                
        if len(output) > 20:
            collength = len(output)/5
            return '''<div class="column">%s</div>
                        <div class="column">%s</div>
                        <div class="column">%s</div>
                        <div class="column">%s</div>
                    <div class="lastcolumn">%s</div>''' % (''.join(output[:collength]), ''.join(output[collength:collength*2]), ''.join(output[collength*2:collength*3]), ''.join(output[collength*3:collength*4]), ''.join(output[collength*4:]))
        elif len(output):
            return '<div class="column">%s</div>' % ''.join(output)
        else:
            return '<div></div>'    
            
            
    def _check_store(self, form):
        id = form.get('id', None)
        fullid = '%s-%s' % (id, session.user.username)
        if id != None:
            exists = 'false'
            for r in editStore:
                if r.id == fullid:
                    exists = 'true'
                    break;              
            if exists == 'false':                                  
                for r in editStore:
                    if r.id[:r.id.rfind('-')] == id :
                        exists = 'true'
                        owner = r.id[r.id.rfind('-')+1:]
                        break;
                return '<wrapper><value>%s</value><owner>%s</owner></wrapper>' % (exists, owner)
            else:
                return '<wrapper><value>%s</value><owner>user</owner></wrapper>' % exists                  


    def _check_directory(self, form):
        id = form.get('id', None)
        fullid = '%s.xml' % id
        if os.path.exists('%s/%s' % (sourceDir, fullid)):
            return 'true'
        else:
            return 'false'
                         

            
#
# End of AJAX calls        
##########################################################################################  
 
#SUBMIT FUNCTIONS

    def submit(self, req, form):
        operation = form.get('operation', 'index')
        owner = form.get('owner', session.user.username)
        session.database = db.id
        pagesize = 20
        req.content_type = 'text/html'
        req.send_http_header()
        head = unicode(read_file('header.html'))
        nav = unicode(read_file('editNav.html'))
        req.write(head)     
        req.write(nav)
        req.write('<div id="maincontent">')
        
        if operation == 'index' and os.path.exists(lockfilepath):
            req.write('<p><span class="error">[ERROR]</span> - Another user is already indexing this database so no files can currently be submitted. Please try again in 10 minutes.</p>\n<p><a href="menu.html">Back to \'Main Menu\' page.</a></p>')
        else :  
            #do initialisation stuff create rec etc.
            preparseWorkflow = db.get_object(session, 'preParserWorkflow')
            indexWorkflow = db.get_object(session, 'indexRecordWorkflow')
            
            recid = form.get('1', None)
            rec = xmlp.process_document(session, StringDocument(self.build_marc(form, '959')))
            rec.id = recid
            
           
            if operation == 'index':                
                lock = open(lockfilepath, 'w')
                lock.close() 
                try:
                    self.logger.log('Preparing to index file')
                    #delete and unindex the old version from the record store
                    try : 
                        oldRec = recordStore.fetch_record(session, recid)
                    except :
                        self.logger.log('New record - nothing to unindex')
                        #this is a new record so we don't need to delete anything
                        exists = False
                        req.write('looking for record... <span class="ok">[OK]</span> - New Record <br/>\n')
                    else :
                        self.logger.log('Unindexing existing record')
                        req.write('undindexing existing version of record... ')
                        db.unindex_record(session, oldRec)
                        req.write('record unindexed')
                        db.remove_record(session, oldRec)
                        req.write('<span class="ok">[OK]</span><br/>\nDeleting record from stores...')
                        self.logger.log('file unindexed')
                        recordStore.begin_storing(session)
                        recordStore.delete_record(session, oldRec.id)
                        recordStore.commit_storing(session)
                        self.logger.log('deleted from record store')
                                              
                    #add and index new record
                    self.logger.log('indexing new record')
                    req.write('indexing new record... ')
                    
                    db.begin_indexing(session)
                    recordStore.begin_storing(session)

                    recordStore.store_record(session, rec)
                    #add workflow processing here
                    doc = preparseWorkflow.process(session, StringDocument(rec.get_xml(session)))
                    rec = xmlp.process_document(session, doc)
                    indexWorkflow.process(session, rec)

                    recordStore.commit_storing(session)

                    db.commit_indexing(session)
                    db.commit_metadata(session)   
                    req.write('<span class="ok">[OK]</span><br/>\n')       
                    
                finally:
                    if os.path.exists(lockfilepath):
                        os.remove(lockfilepath)  
        #write to file
        filepath = '%s/%s.xml' % (sourceDir, recid)
        req.write('Writing to file system... ')
        if (os.path.exists(filepath)):
            os.remove(filepath)
        file = open(filepath, 'w')
        file.write(rec.get_xml(session))
        file.flush()
        file.close()
        req.write('<span class="ok">[OK]</span><br/>\n')  
        #remove from editStore
        req.write('Removing from draft store... ')
        editStore.begin_storing(session)
        editStore.delete_record(session, '%s-%s' % (recid, owner))
        editStore.commit_storing(session)
        req.write('<span class="ok">[OK]</span><br/>\n')
        
       #retrieve cookie and set link back to results     
        cookie = Cookie.get_cookies(req, Cookie.Cookie)
        if cookie.has_key('searchResults'):
            values = cookie['searchResults'].value.split('-')
            rsid = values[0]
            id = values[1]
            
            #calculate start value
            stringid = str(id)
            if len(stringid) > 1:
                lastdigit = stringid[-1]
                id = int(id) - int(lastdigit)
                if id % pagesize == 0:
                    start = id
                else:
                    start = id-pagesize/2
            else:
                start = 0
            
            
            req.write('<p><a href="../search/search.html?operation=search&rsid=%s&start=%s">Back to Search Results</a></p>' % (rsid, start))
        
        req.write('<p><a href="menu.html">Back to \'Main Menu\' page.</a></p>')
        foot = unicode(read_file('footer.html'))
        req.write('</div>')      
        req.write(foot)
        return None
            
        


    def replace_ref(self, abbrev, full):
        session.database = dbrefs.id
        refsStore = dbrefs.get_object(session, 'refsRecordStore')
        entry = StringDocument('<record><code>%s</code><full>%s</full></record>' % (abbrev, full))  
        newRec = xmlp.process_document(session, entry)
        
        q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (abbrev))     
        rs = dbrefs.search(session, q)
        recid = None
        try:
            rec = rs[0].fetch_record(session)
        except:
            pass
        else:
            recid = rec.id
            dbrefs.unindex_record(session, rec)
            dbrefs.remove_record(session, rec)
            refsStore.begin_storing(session)
            refsStore.delete_record(session, rec.id)
            refsStore.commit_storing(session)
            
        dbrefs.begin_indexing(session)
        refsStore.begin_storing(session)  
        if recid == None:     
            indexFlow = dbrefs.get_object(session, 'refsIndexRecordWorkflow')          
        else:
            indexFlow = dbrefs.get_object(session, 'refsIndexExistingRecordWorkflow')
        indexFlow.process(session, newRec)     
        refsStore.commit_storing(session)
        dbrefs.commit_indexing(session)
        dbrefs.commit_metadata(session)
        filename = '/home/cheshire/cheshire3/dbs/istc/refsData/refs.xml'
        os.rename(filename, '/home/cheshire/cheshire3/dbs/istc/refsData/refs.bak')
        file = open(filename, 'w')
            
        for r in refsStore:
            file.write(r.get_xml(session)) 
        file.flush()
        file.close()
            
            
    def submit_refsub(self, form):     
        abbrev = form.get('abbrev', '')
        full = form.get('full', '')
        if os.path.exists(reflockfilepath):
            return 'locked'
        else :  
            lock = open(reflockfilepath, 'w')
            lock.close() 
            success = False
            try:
                self.replace_ref(abbrev, full)
                success = True            
            finally:
                if os.path.exists(reflockfilepath):
                    os.remove(reflockfilepath)  
            if success == True:
                return 'success'
            else:
                return 'failed' 
            
            
    def submit_ref(self, req, form):
        abbrev = form.get('abbrev', '')
        full = form.get('full', '')
        req.content_type = 'text/html'
        req.send_http_header()
        head = unicode(read_file('header.html'))
        nav = unicode(read_file('editNav.html'))
        req.write(head)     
        req.write(nav)
        req.write('<div id="maincontent">')
        req.write('<p>Processing Request...</p>')
        if abbrev.strip() == '' or full.strip() == '':
            return 
        if os.path.exists(reflockfilepath):
            req.write('<p><span class="error">[ERROR]</span> - Another user is already indexing this database so no files can currently be indexed. Please try again in 10 minutes.</p>\n<p><a href="menu.html">Back to \'Main Menu\' page.</a></p>')
        else :  
            lock = open(reflockfilepath, 'w')
            lock.close() 
            success = False
            try:
                self.replace_ref(abbrev, full)
                success = True
            finally:
                if os.path.exists(reflockfilepath):
                    os.remove(reflockfilepath)  
            if success == True:
                req.write('<p><span class="ok">[OK]</span> - The Bibliographical References have been successfully updated.</p>\n<p><a href="menu.html">Back to \'Main Menu\' page.</a></p>')           
            else :
                req.write('<p><span class="error">[ERROR]</span> - There was a problem while updating the Bibliographical References. Please contact John Goldfinch.</p>\n<p><a href="menu.html">Back to \'Main Menu\' page.</a></p>')

        foot = unicode(read_file('footer.html'))   
        req.write('</div>')      
        req.write(foot)
        return None
    
    
    def replace_usa(self, abbrev, full):
        session.database = dbusa.id
        usaStore = dbusa.get_object(session, 'usaRecordStore')
        entry = StringDocument('<record><code>%s</code><full>%s</full></record>' % (abbrev, full))  
        newRec = xmlp.process_document(session, entry)
        
        q = qf.get_query(session, 'c3.idx-key-usa exact "%s"' % (abbrev))     
        rs = dbusa.search(session, q)
        recid = None
        try:
            rec = rs[0].fetch_record(session)
        except:
            pass
        else:
            recid = rec.id
            dbusa.unindex_record(session, rec)
            dbusa.remove_record(session, rec)
            usaStore.begin_storing(session)
            usaStore.delete_record(session, rec.id)
            usaStore.commit_storing(session)
            
        dbusa.begin_indexing(session)
        usaStore.begin_storing(session)  
        if recid == None:     
            indexFlow = dbusa.get_object(session, 'usaIndexRecordWorkflow')          
        else:
            indexFlow = dbusa.get_object(session, 'usaIndexExistingRecordWorkflow')
        indexFlow.process(session, newRec)     
        usaStore.commit_storing(session)
        dbusa.commit_indexing(session)
        dbusa.commit_metadata(session)
        filename = '/home/cheshire/cheshire3/dbs/istc/usaData/usaCodes.xml'
        os.rename(filename, '/home/cheshire/cheshire3/dbs/istc/usaData/usaCodes.bak')
        file = open(filename, 'w')
            
        for r in usaStore:
            file.write(r.get_xml(session)) 
        file.flush()
        file.close()
            
            
    def submit_usasub(self, form):     
        abbrev = form.get('abbrev', '')
        full = form.get('full', '')
        if os.path.exists(usalockfilepath):
            return 'locked'
        else :  
            lock = open(usalockfilepath, 'w')
            lock.close() 
            success = False
            try:
                self.replace_usa(abbrev, full)
                success = True            
            finally:
                if os.path.exists(usalockfilepath):
                    os.remove(usalockfilepath)  
            if success == True:
                return 'success'
            else:
                return 'failed' 
            
            
    def submit_usa(self, req, form):
        abbrev = form.get('abbrev', '')
        full = form.get('full', '')
        req.content_type = 'text/html'
        req.send_http_header()
        head = unicode(read_file('header.html'))
        nav = unicode(read_file('editNav.html'))
        req.write(head)     
        req.write(nav)
        req.write('<div id="maincontent">')
        req.write('<p>Processing Request...</p>')
        if abbrev.strip() == '' or full.strip() == '':
            return 
        if os.path.exists(usalockfilepath):
            req.write('<p><span class="error">[ERROR]</span> - Another user is already indexing this database so no files can currently be indexed. Please try again in 10 minutes.</p>\n<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')
        else :  
            lock = open(usalockfilepath, 'w')
            lock.close() 
            success = False
            try:
                self.replace_usa(abbrev, full)
                success = True
            finally:
                if os.path.exists(usalockfilepath):
                    os.remove(usalockfilepath)  
            if success == True:
                req.write('<p><span class="ok">[OK]</span> - The USA Locations have been successfully updated.</p>\n<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')           
            else :
                req.write('<p><span class="error">[ERROR]</span> - There was a problem while updating the USA Locations. Please contact John Goldfinch.</p>\n<p><a href="menu.html">Back to \'Main Menu\'.</a></p>')

        foot = unicode(read_file('footer.html'))   
        req.write('</div>')      
        req.write(foot)
        return None    
    
    
    
    
    
# End of SUBMIT FUNCTIONS     
########################################################################################## 

                
    def handle(self, req):
        form = FieldStorage(req, True)  
                
        tmpl = unicode(read_file(self.baseTemplatePath))
        nav = unicode(read_file(self.editNavPath))
        tmpl = tmpl.replace('%NAVIGATION%', nav)
        
        path = req.uri[1:] 
        path = path[path.rfind('/')+1:]
        
        content = None      
        operation = form.get('operation', None)
        
        if (operation) : 
            if (operation == 'create'):
                content = self.generate_file(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif (operation == 'edit'):
                content = self.edit_file(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif (operation == 'load'):
                content = self.load_file(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif (operation == 'suggest'):
                content = self._get_suggestions(form)
                self.send_xml(content, req)
            elif (operation == 'all'):
                content = self._get_all(form)
                self.send_xml(content, req) 
            elif (operation == 'checkStore'):
                content = self._check_store(form)
                self.send_xml(content, req)  
            elif (operation == 'checkDir'):
                content = self._check_directory(form)
                self.send_xml(content, req)              
            elif operation == 'save':
                content = self.save(form)
                self.send_xml(content, req)
                return
            elif operation == 'xml':
                content = self.preview_xml(form)
                self.send_xml(content, req)
                return
            elif operation == 'email':
                content = self.email(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif operation == 'marc':
                content = self.preview_marc(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif operation == 'file' or operation == 'index':
                content = self.submit(req, form)
                
            elif operation == 'edituser':
                content = self.edit_user(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif operation == 'discard':
                content = self.delete(form)
                content = tmpl.replace('%CONTENT%', content)
                self.send_html(content, req)
            elif operation == 'refsubform':
                content = self.get_refForm(form)
                self.send_html(content, req)
            elif operation == 'submitrefsub':
                content = self.submit_refsub(form)
                self.send_xml(content, req)
            elif operation == 'submitref':
                content = self.submit_ref(req, form)
            elif operation == 'submitusasub':
                content = self.submit_usasub(form)
                self.send_xml(content, req)
            elif operation == 'submitusa':
                content = self.submit_usa(req, form)
            elif (operation == 'references'):
                content = self.get_fullRefs(session, form)
                self.send_xml(content, req)
                return
            elif (operation == 'usa'):
                content = self.get_fullUsa(session, form)
                self.send_xml(content, req)
                return
            elif (operation.strip() == 'Delete' or operation.strip() == 'Delete + Unindex'):
                content = self.delete_file(req, form)
            
        else:
            if path == 'edit.html':
                content = self.show_editMenu('edit')
            elif path == 'delete.html':
                content = self.show_editMenu('delete')
            elif path == 'editref.html':
                content = self.show_editMenu('editref')
            elif path == 'editusa.html':
                content = self.show_editMenu('editusa')
            elif path == 'editusermenu.html':
                content = self.show_editMenu('user')
            elif path == 'edithelp.html':
                f= file("edithelp.html")
                content = f.read()
                f.close()
            else:
                content = self.show_editMenu('main')
            
            
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
    global session, serv, db, dbusa, dbrefs, qf, editStore, recordStore, noteStore, authStore, formTxr, xmlp, indentingTxr, sourceDir, lockfilepath, reflockfilepath, usalockfilepath
#    
#    if editStore:
#        editStore.commit_storing(session)
#    if noteStore:
#        noteStore.commit_storing(session)
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
#    session.user = None
    serv = SimpleServer(session, cheshirePath + '/cheshire3/configs/serverConfig.xml')
    db = serv.get_object(session, 'db_istc')
    dbusa = serv.get_object(session, 'db_usa')
    dbrefs = serv.get_object(session, 'db_refs')
    qf = db.get_object(session, 'baseQueryFactory')
    baseDocFac = db.get_object(session, 'istcDocumentFactory')
    sourceDir = baseDocFac.get_default(session, 'data')
    editStore = db.get_object(session, 'editingStore')
    recordStore = db.get_object(session, 'recordStore')
    noteStore = db.get_object(session, 'notesStore')
    authStore = db.get_object(session, 'istcAuthStore')
    xmlp = db.get_object(session, 'LxmlParser')
    formTxr = db.get_object(session, 'formCreationTxr')
    indentingTxr = db.get_object(session, 'indentingTxr')
    
    rebuild = False
    
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
        lgr = FileLogger(cheshirePath + '/cheshire3/www/istc/logs/edithandler.log', remote_host)                                  # initialise logger object
        istcEditingHandler = IstcEditingHandler(lgr)                                      # initialise handler - with logger for this request
        try:
            istcEditingHandler.handle(req)   
        finally:
            try:
                lgr.flush()
            except:
                pass
            del lgr, istcEditingHandler                                          # handle request
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
    