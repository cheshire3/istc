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
import sys
sys.path.insert(1,'/home/cheshire/cheshire3/code')
from istcHandler import *
from crypt import crypt

class IstcAdminHandler(IstcHandler):
    
    def __init__(self, lgr):
        IstcHandler.__init__(self, lgr)
#        if (rebuild):
#            build_architecture()
            
        self.logger = lgr

    
    def handle(self, req):
        session = Session()
        session.environment = "apache"
        session.server = serv
                
        form = FieldStorage(req)

        #get the template 
        f = file(self.templatePath)
        tmpl = f.read()
        f.close()
        tmpl = tmpl.replace('\n', '')
               
        path = req.uri[1:] 
        path = path[path.rfind('/')+1:]
        
        operation = form.get('operation', None)
        e = ""
        rl = ""
        if path == 'search.html':
            if operation:
                if (operation == 'record'):
                    (t, d, e, rl) = self.display_rec(session, form)
                elif (operation == 'search'):
                    (t, d, e) = self.handle_istc(session, form)
                elif (operation == 'print'):
                    data = self.printRecs(form)
                    self.send_html(data, req)
                    return
                elif (operation == 'email'):
                    (t, d, e) = self.emailRecs(form)
                elif (operation == 'save'):
                    data = self.saveRecs(form)
                    self.send_txt(data, req)
                    return
                elif (operation == 'format'):
                    content = self.get_format(session, form)
                    self.send_xml(content, req)
                    return
                else:
                    content = 'An invalid operation was attempted.'
                    self.send_html(content, req)
                    return
            else:
                f= file("index.html")
                t = "Search"
                d = f.read()
                f.close()
        elif path == 'browse.html':
            if operation:
                if operation == 'scan':
                    (t, d) = self.browse(form)
                else:
                    content = 'An invalid operation was attempted.'
                    self.send_html(content, req)
                    return
            else:
                f = file('browse.html')
                t = "Browse"
                d = f.read()
                f.close()
        elif path == 'about.html':
            f = file('about.html')
            t = "About the Catalogue"
            d = f.read()
            f.close()
            
        else:
            f= file("index.html")
            t = "Search"
            d = f.read()
            f.close()    
        extra = '' #TODO check if this is needed - not sure %EXTRA% ever exists
 #       raise ValueError(d)
 #       d = d.encode('utf8')
 #       d = d.replace('iso-8859-1', 'utf-8')
 #       e = e.encode('utf8')
        tmpl = tmpl.replace("%CONTENT%", d)
        tmpl = tmpl.replace("%CONTENTTITLE%", t)
        tmpl = tmpl.replace("%EXTRA%", extra)
        tmpl = tmpl.replace("%EXTRATABLESTUFF%", e)
        tmpl = tmpl.replace('%BACKTORESULTLIST%', rl)

        self.send_html(tmpl, req)

rebuild = True
serv = None
session = None
db = None
qf = None
baseDocFac = None
sourceDir = None
editStore = None
recordStore = None
authStore = None
xmlp = None
formTxr = None
indentingTxr = None


def build_architecture(data=None):
    global session, serv, db, qf, editStore, recordStore, authStore, formTxr, xmlp, indentingTxr, sourceDir
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
    session.user = None
    serv = SimpleServer(session, cheshirePath + '/cheshire3/configs/serverConfig.xml')
    db = serv.get_object(session, 'db_istc')
    qf = db.get_object(session, 'baseQueryFactory')
    baseDocFac = db.get_object(session, 'baseDocumentFactory')
    sourceDir = baseDocFac.get_default(session, 'data')
    editStore = db.get_object(session, 'editingStore')
    recordStore = db.get_object(session, 'recordStore')
    authStore = db.get_object(session, 'istcAuthStore')
    xmlp = db.get_object(session, 'LxmlParser')
    formTxr = db.get_object(session, 'formCreationTxr')
    indentingTxr = db.get_object(session, 'indentingTxr')
    rebuild = False
    
    logfilepath = cheshirePath + '/cheshire3/www/istc/logs/edithandler.log'




def handler(req):
    global rebuild, logfilepath, cheshirePath, db, editStore, xmlp, formTxr, script                # get the remote host's IP
    script = req.subprocess_env['SCRIPT_NAME']
    req.register_cleanup(build_architecture)

    try :
        if rebuild:
            build_architecture()

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