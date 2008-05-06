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


    def generate_file(self, form):
        structure = read_file('editTemplate.html')
        doc = StringDocument('<record></record>')         
        rec = xmlp.process_document(session, doc)
        page = formTxr.process_record(session, rec).get_raw(session)
        page = structure.replace('%CONTENT%', page)
        return page


    def build_marc(self, form):
        tree = etree.fromstring('<record></record>')
#        ctype = form.get('ctype', None)
#        level = form.get('location', None)
#        collection = False;
#        if (level == 'collectionLevel'):
#            collection = True;
#            tree = etree.fromstring('<ead><eadheader></eadheader><archdesc></archdesc></ead>')           
#            header = tree.xpath('/ead/eadheader')[0]
#            target = self._create_path(header, 'eadid')
#            if form.get('eadid', '') != '':
#                self._add_text(target, form.get('eadid', ''))
#            else :
#                self._add_text(target, form.get('pui', ''))
#            target = self._create_path(header, 'filedesc/titlestmt/titleproper')
#            self._add_text(target, form.get('did/unittitle', ''))     
#            if form.get('filedesc/titlestmt/sponsor', '') != '': 
#                target = self._create_path(header, 'filedesc/titlestmt/sponsor')   
#                self._add_text(target, form.get('filedesc/titlestmt/sponsor', '')) 
#            target = self._create_path(header, 'profiledesc/creation')
#            if session.user.realName != '' :
#                userName = session.user.realName
#            else :
#                userName = session.user.username
#            self._add_text(target, 'Created by %s using the cheshire for archives ead creation tool ' % userName)
#            target = self._create_path(header, 'profiledesc/creation/date')
#            self._add_text(target, '%s' % datetime.date.today())
#        else :
#            tree = etree.fromstring('<%s id="%s"></%s>' % (ctype, level, ctype))           
        list = form.list     
        for field in list :
            if field.name not in []:        
                #do did level stuff              
                node = tree.xpath('/record]')[0]
                if field.name.find('controlaccess') == 0 :
                    self._create_controlaccess(node, field.name, field.value) 
                elif field.name.find('did/langmaterial') == 0 :
                    did = self._create_path(node, 'did')
                    self._create_langmaterial(did, field.value)
                else :
                    if (field.value.strip() != '' and field.value.strip() != ' '):
                        target = self._create_path(node, field.name)
                        self._add_text(target, field.value)
        return tree    
    #- end build_marc
    
    
    def _create_path(self, startNode, nodePath):              
        if (startNode.xpath(nodePath)):
            if (nodePath.find('@') == -1):
                return startNode.xpath(nodePath)[0]
            else :  
                if len(startNode.xpath(nodePath[:nodePath.rfind('/')])) > 0:
                    parent = startNode.xpath(nodePath[:nodePath.rfind('/')])[0]
                else :
                    parent = startNode
                attribute = nodePath[nodePath.rfind('@')+1:]
                return [parent, attribute]
        elif (nodePath.find('@') == 0):
            return self._add_attribute(startNode, nodePath[1:])
        elif (nodePath.find('/') == -1) :
            if nodePath.find('[') != -1 :
                newNode = etree.Element(nodePath[:nodePath.find('[')])   
            else :
                newNode = etree.Element(nodePath)                     
            return self._append_element(startNode, newNode)
        else :
            newNodePath = ''.join(nodePath[:nodePath.rfind('/')]) 
            nodeString = ''.join(nodePath[nodePath.rfind('/')+1:])  
            if (nodeString.find('@') != 0):      
                if nodeString.find('[') != -1 :
                    newNode = etree.Element(nodeString[:nodeString.find('[')])
                else :
                    newNode = etree.Element(nodeString)
                return self._append_element(self._create_path(startNode, newNodePath), newNode)
            else:
                return self._add_attribute(self._create_path(startNode, newNodePath), nodeString[1:])  
            
                        
    def _append_element(self, parentNode, childNode):    
        parentNode.append(childNode)
        return childNode

    
    def _add_attribute(self, parentNode, attribute):
        parentNode.attrib[attribute] = ""
        return [parentNode, attribute]


    def _add_text(self, parent, textValue):
        if not (textValue.find('&') == -1):
            textValue = textValue.replace('&', '&#38;')
        textValue = textValue.lstrip()      
        if isinstance(parent, etree._Element):
            for c in parent.getchildren() :
                parent.remove(c)
            value = '<foo>%s</foo>' % textValue      
            try :
                nodetree = etree.fromstring(value)               
            except :
                self.errorFields.append(parent.tag)
                parent.text = textValue
            else :
                parent.text = nodetree.text
                for n in nodetree :
                    parent.append(n)
        else :
            parent[0].attrib[parent[1]] = textValue
            
            
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
        
            
    def handle(self, req):
        form = FieldStorage(req, True)  
        tmpl = read_file(templatePath)
        content = None      
        operation = form.get('operation', None)
        if (operation == 'display'):
            content = self.display(req)
            self.send_html(content, req)
        else:
            content = self.generate_file(form)
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
    global session, serv, db, editStore, recordStore, authStore, formTxr, xmlp, indentingTxr
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
    session.user = None
    serv = SimpleServer(session, '/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml')
    db = serv.get_object(session, 'db_istc')
    baseDocFac = db.get_object(session, 'defaultDocumentFactory')
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