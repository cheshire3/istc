from mod_python import apache, Cookie
from mod_python.util import FieldStorage
import sys, os, cgitb, time, re

from baseObjects import Session
from server import SimpleServer
from PyZ3950 import CQLParser
from baseObjects import Session
from utils import flattenTexts
from document import StringDocument
from record import LxmlRecord
from www_utils import *
from lxml import etree
#from wwwSearch import *
from crypt import crypt
from istcLocalConfig import *

class IstcEditingHandler:
    templatePath = "/home/cheshire/cheshire3/cheshire3/www/istc/html/template.ssi"
    
    
    def __init__(self, lgr):
        self.logger = lgr
    
    
    def send_html(self, text, req, code=200):
        req.content_type = 'text/html; charset=utf-8'
        req.content_length = len(text)
        req.send_http_header()
        req.write(text)


    def send_xml(self, data, req, code=200):
        req.content_type = 'text/xml'
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()       
    #- end send_xml()


    def generate_file(self, form):
        structure = read_file('editTemplate.html')
        doc = StringDocument('<record></record>')         
        rec = xmlp.process_document(session, doc)
        page = formTxr.process_record(session, rec).get_raw(session)
        page = structure.replace('%CONTENT%', page)
        return page
         
            
    def display(self, form):
        rec = self.save(form)
        doc = indentingTxr.process_record(session, rec)
        raise ValueErorr(doc.get_raw(session))


    def save(self, form):
        recid = form.get("controlfield[@tag='001']", None)
        try:
            retrievedRec = editStore.fetch_record(session, recid)
        except:
            rec = LxmlRecord(self.build_ead(form))
            rec.id = recid
            editStore.store_record(session, rec)
            editStore.commit_storing(session)
            return rec
        
        
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
                out.extend(['<li>'
                           ,'<span class="fileops"><input type="%s" name="recid" value="%s"/></span>' % (type, s.id)
                           ,'<span class="filename">%s</span>' % s.id
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
                userFiles = ['<li title=%s><span>%s</span>' % (name, name), '<ul class="hierarchy">'] 
                for s in store:
                    if s.id[s.id.rfind('-')+1:] == name:
                        userFiles.extend(['<li>'
                                           ,'<span class="fileops"><input type="%s" name="recid" value="%s" %s/></span>' % (type, s.id, disabled)
                                           ,'<span class="filename">%s</span>' % s.id
                                           ,'</li>'
                                           ])
                        total += 1;
                userFiles.append('</ul></li>')
                out.append(''.join(userFiles))
            if total < store.get_dbSize(session):
                if session.user.has_flag(session, 'info:srw/operation/1/create', 'eadAuthStore'):
                    disabled = ''
                else :
                    disabled = 'disabled="disabled"'
                for s in store:
                    if s.id[s.id.rfind('-')+1:] not in names:
                        out.extend(['<li title=deletedUsers><span>Deleted Users</span>', '<ul class="hierarchy">', '<li>'
                                                   ,'<span class="fileops"><input type="%s" name="recid" value="%s" %s/></span>' % (type, s.id, disabled)
                                                   ,'<span class="filename">%s</span>' % s.id
                                                   ,'</li>'])
            return out
                
    
    def edit_file(self, form):
        f = form.get('filepath', None)
        if not f or not len(f.value):
            #TODO: create appropriate html file - this is for admin
            return read_file('upload.html')
        ws = re.compile('[\s]+')
        xml = ws.sub(' ', read_file(f))
        doc = StringDocument(xml)      
        rec = xmlp.process_document(session, doc)
        
        # TODO: handle file not successfully parsed
        if not isinstance(rec, LxmlRecord):
            return rec     
        istcNo = rec.process_xpath(session, '//controlfield[@tag="001"]/text()')[0]
        rec.id = istcNo
        editStore.store_record(session, rec)
        editStore.commit_storing(session) 
        structure = read_file('editTemplate.html')
        page = formTxr.process_record(session, rec).get_raw(session)
        page = structure.replace('%CONTENT%', page)
        return page

           
    def show_editMenu(self):
        global sourceDir
        self.logger.log('Create/Edit Options')
        page = read_file('editmenu.html')
        files = self._walk_directory(sourceDir, 'radio')
        recids = self._walk_store('editingStore', 'radio')  

        assignmentOptn = ''
        return multiReplace(page, {'%%%SOURCEDIR%%%': sourceDir, '%%%FILES%%%': ''.join(files), '%%%RECORDS%%%': ''.join(recids), '%%%USROPTNS%%%': assignmentOptn})
 
 
    def _cleverTitleCase(self, txt):
        words = txt.split()
        for x in range(len(words)):
            if (x == 0 and not words[x][0].isdigit()) or (words[x][0].isalpha()) and (words[x] not in ['de']):
                words[x] = words[x].title()
        return ' '.join(words)
 
 
##########################################################################################
# AJAX calls 
#


    def _get_suggestions(self, form):
        letters = form.get('s', None)
        index = form.get('i', None)
        q = CQLParser.parse('c3.%s = %s' % (index, letters))
        idx = db.get_object(session, '%s' % index)
        terms = db.scan(session, q, -1, direction="=")
        output = []
        for t in terms:
            term = self._cleverTitleCase(t[0])
            output.append('%s (%i)' % (term, t[1][1]))
            #TODO: check that t[1][1] is actually no of occs not no of recs (may need to be t[1][2])
        return '<select>%s</select>' % ' | '.join(output)
            
            
#
# End of AJAX calls        
##########################################################################################      
        
                
    def handle(self, req):
        form = FieldStorage(req, True)  
        tmpl = read_file(templatePath)
        content = None      
        operation = form.get('operation', None)
        if (operation) : 
            if (operation == 'display'):
                content = self.display(req)
                self.send_html(content, req)
            elif (operation == 'create'):
                content = self.generate_file(form)
                self.send_html(content, req)
            elif (operation == 'edit'):
                content = self.edit_file(form)
                self.send_html(content, req)
            elif (operation == 'suggest'):
                content = self._get_suggestions(form)
                self.send_xml(content, req)
        else:
            content = self.show_editMenu()
            # send the display
            self.send_html(content, req)
    
rebuild = True
serv = None
session = None
db = None
baseDocFac = None
sourceDir = None
editStore = None
recordStore = None
authStore = None
xmlp = None
formTxr = None
indentingTxr = None

def build_architecture(data=None):
    global session, serv, db, editStore, recordStore, authStore, formTxr, xmlp, indentingTxr, sourceDir
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
    session.user = None
    serv = SimpleServer(session, '/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml')
    db = serv.get_object(session, 'db_istc')
    baseDocFac = db.get_object(session, 'baseDocumentFactory')
    sourceDir = baseDocFac.get_default(session, 'data')
    editStore = db.get_object(session, 'editingStore')
    recordStore = db.get_object(session, 'recordStore')
    authStore = db.get_object(session, 'istcAuthStore')
    xmlp = db.get_object(session, 'LxmlParser')
    formTxr = db.get_object(session, 'formCreationTxr')
    indentingTxr = db.get_object(session, 'indentingTxr')
    rebuild = False
    
    logfilepath = '/home/cheshire/cheshire3/cheshire3/www/istc/logs/edithandler.log'




def handler(req):
    global rebuild, logfilepath, cheshirePath, db, editStore, xmlp, formTxr, script                # get the remote host's IP
    script = req.subprocess_env['SCRIPT_NAME']
    req.register_cleanup(build_architecture)

    try :

        remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)
        os.chdir(os.path.join(cheshirePath, 'cheshire3', 'www', 'istc', 'html'))     # cd to where html fragments are
        lgr = FileLogger('/home/cheshire/cheshire3/cheshire3/www/istc/logs/edithandler.log', remote_host)                                  # initialise logger object
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