from mod_python import apache, Cookie
from mod_python.util import FieldStorage
import sys, os, cgitb, time, re

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
from lxml import etree
from copy import deepcopy
#from wwwSearch import *
from crypt import crypt
from istcLocalConfig import *

class IstcEditingHandler:
    templatePath = cheshirePath + "/cheshire3/www/istc/html/editTemplate.html"
    
    
    def __init__(self, lgr):
        self.logger = lgr

    def test(self, session, req):
        req.write('starting')
        db.begin_indexing(session)
        req.write('done')    
    
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
        try:
            data = data.encode('utf-8')
        except:
            pass
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


    def build_marc(self, form):
        multipleEntryFields = ['imprints', 'generalnotes', 'references', 'blshelfmarks']
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
                elif l.name in multipleEntryFields:
                    if l.value.find('|||') != -1:
                        meList = l.value.split('|||')
                        ind = '0-0'
                        codelist = []
                        for me in meList:  
                            if me.strip() != '': 
                                temp = me.split('|')
                                code = temp[0].split('_')[1].strip()
                                if code == 'ind':
                                    n = int(temp[0].split('_')[0])
                                    ind = temp[1]
                                else :
                                    codelist.append((code, temp[1].strip()))
                        tuple = ((ind.split('-')[0].strip(), ind.split('-')[1].strip(), codelist))
                        try:
                            marc[n].append(tuple)
                        except:
                            marc[n] = [tuple]
                            
                else:
                    name = l.name.split('_')
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
           
        marcObject = MARC()
        marcObject.fields = marc
        return StringDocument(marcObject.toMARCXML())




       
#        for l in list:
#            if l.value.strip() != '' and l.value.strip() != ' ' and l.name[l.name.find('_'):] != 'ind':
#                if l.name.find('_'):
#                    temp.append(l.name[:l.name.rfind('_')])
#                else:
#                    temp.append(l.name)
#        tags = set(temp)
#        data = []
#        for t in tags:    
#            if t not in ['operation', '001', '008']:
#                for code in enumerate(alph):
#                    field = form2.get('%s_%s' % (t, code), None)
#                    if field != None:
#                        data.append(('%s', '%s') % (code, field.value.strip()))
#                indicators = form2.get('%s_ind' % t, '0|0').split('|')
#                
#                tuple = (indicators[0], indicators[1], data)
#                try :
#                    dict[t].append(tuple)
#                except:
#                    dict[t] = [tuple]
#        raise ValueError(dict)
                

    def save(self, form):
        recid = form.get("controlfield[@tag='001']", None)
        try:
            retrievedRec = editStore.fetch_record(session, recid)
        except:
            rec = xmlp.process_document(session, self.build_marc(form))
            raise ValueError(rec.get_xml(session))
            rec.id = recid
            editStore.store_record(session, rec)
            editStore.commit_storing(session)
            return rec
 
 
    def get_fullRefs(self, session, form, recursive=True):
        ref = form.get('q', None)
        ref = ref.replace('*', '\*')
        ref = ref.replace('?', '\?')        
        r = form.get('r', '') 
        if r != '':
            recursive=False
        session.database = db3.id
        q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (ref))
        rs = db3.search(session, q)
        if len(rs):
            recRefs = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
        else :
            if recursive :
                while ref.rfind(' ') != -1 and not len(rs):
                    ref = ref[:ref.rfind(' ')].strip()
                    q.term.value = ref.decode('utf-8')
                    rs = db3.search(session, q)
                if len(rs):
                    recRefs = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
                else:
                    recRefs = '' 
            else:
                recRefs = '' 
        return recRefs

       
        
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
        dataPath = cheshirePath + '/cheshire3/dbs/istc/data/'
        f = '%s%s.xml' % (dataPath, form.get('q', None))
#       if not f or not len(f.value):
#            #TODO: create appropriate html file - this is for admin
#            return read_file('upload.html')
        xml = read_file(f)
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
        page = page.replace('%RFRNC%', self._get_refxml(session, rec))
        page = structure.replace('%CONTENT%', page)
        return page


    def _get_refxml(self, session, rec):
        bibRefNormalizer = db.get_object(session, 'BibRefNormalizer')
        f510 = rec.process_xpath(session, '//datafield[@tag ="510"]/subfield/text()')
        if not len(f510):
            return '<div id="addedreferences" style="display:none" class="added" onmouseout="getFormRef()"><ul id="addedreferenceslist"></ul></div>'
        else:
            output = []
            for index, t in enumerate(f510):
                abbrev = bibRefNormalizer.process_string(session, t)
                other = t[len(abbrev) + 1:]
                session.database = db3.id
                q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (abbrev))
                rs = db3.search(session, q)
                if len(rs):
                    full =  rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
                else:
                    full = abbrev
                hidden = '510_a | %s ||| 510_other | %s ||| 510_ind | 4-0 ||| ' % (abbrev, other)
                
                output.extend(['<li style="position: relative;" id="lireferences_formgen%d">' % index ,
                               '<div id="references_formgen%d">' % index,
                               '<div class="icons"><a onclick="deleteEntry(\'references_formgen%d\');" title="delete entry">' % index,
                               '<img src="/istc/images/deletesmall.gif" id="delete%d" />' % index,
                               '</a> <span class="handle">move</span></div>',
                               '<div class="multipleEntry">',
                               '<p class="float" onclick="editEntry(\'references_formgen\', %d);" title="%s">' % (index, full.encode('utf-8')),
                               '%s %s' % (abbrev, other),
                               '</p></div></div>',
                               '<br id="references_formgen%dbr">' % index,
                               '<input id="references_formgen%dxml" name="references" value="%s" type="hidden" />' % (index, hidden),
                               '</li>'])
            return '<div style="display: block;" class="added" id="addedreferences"><ul id="addedreferenceslist">%s</ul></div>' % ' '.join(output)
           
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
        if index == 'idx-key-refs-exact':
            session.db = db3.id
            q = qf.get_query(session, 'c3.%s = "%s"' % (index, letters))
           # idx = db3.get_object(session, '%s' % index)
            terms = db3.scan(session, q, 50, direction="=")            
        else:
            q = qf.get_query(session, 'c3.%s = "%s"' % (index, letters))
          #  idx = db.get_object(session, '%s' % index)
            terms = db.scan(session, q, 50, direction="=")
        output = []
        for t in terms:
            # term = self._cleverTitleCase(t[0])
            term = t[0]
            output.append('%s (%i)' % (term, t[1][1]))
            #TODO: check that t[1][1] is actually no of occs not no of recs (may need to be t[1][2])
        if len(output):
            return '<select>%s</select>' % ' | '.join(output)
        else:
            return '<select></select>'    
            
#
# End of AJAX calls        
##########################################################################################  


#SUB-FORM FUNCTIONS

    
    def get_refForm(self, form):
        page = read_file('refSubForm.html')
        page = page.replace('%%ABBREV%%', form.get('abbrev', ''))
        page = page.replace('%%FULL%%', form.get('full', ''))
        return page
    
#    
#    def submitRef(self, form):
#        abbrev = form.get('abbrev', '')
#        full = form.get('full', '')
#        if abbrev.strip() == '' or full.strip() == '':
#            return self.get_refForm(form)
#        entry = '<record><code>%s</code><full>%s</full></record>' % (abbrev, full)
#        session.database = db3.id
#        q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (abbrev))     
#        rs = db3.search(session, q)
#        if len(rs):
#            
#        else :
#            while ref.rfind(' ') != -1 and not len(rs):
#                ref = ref[:ref.rfind(' ')].strip()
#                q.term.value = ref.decode('utf-8')
#                rs = db3.search(session, q)
#            if len(rs):
#                recRefs = rs[0].fetch_record(session).process_xpath(session, '//full/text()')[0]
#            else:
#                recRefs = 'none' 
#        
#        filename = cheshirePath + 'cheshire3/dbs/istc/refsData/refs.xml'
#        file = open(filename, mode='a', bufsize=1)
#        file.write(entry)
        

#
#    
#    def submit(self, req, form):
#        global sourceDir, ppFlow, xmlp
#        req.content_type = 'text/html'
#        req.send_http_header()
#        head = self._get_genericHtml('header.html')
#        req.write(head)
#        i = form.get('index', 'true')
#        if i == 'false' :
#            index = False
#        else :
#            index = True
#        recid = form.get('recid', None)
#        fileOwner = form.get('owner', session.user.username)
#        editRecid = '%s-%s' % (recid.value, fileOwner)
#        
#        rec = editStore.fetch_record(session, editRecid)
#        
#        filename = form.get('filename', self._get_filename(rec))
#        if filename == None:
#            filename = '%s.xml' % recid
#        
#        xml = rec.get_xml(session)    
#        valid = self.validate_record(xml)     
#        exists = True 
#        if valid and index:
#            #delete and unindex the old version from the record store
#            try : 
#                oldRec = recordStore.fetch_record(session, recid)
#            except :
#                #this is a new record so we don't need to delete anything
#                exists = False
#                req.write('<span class="error">[ERROR]</span> - Record not present in recordStore<br/>\n')
#            else :
#                req.write('undindexing existing version of record... ')
#                db.unindex_record(session, oldRec)
#                req.write('record unindexed')
#                db.remove_record(session, oldRec)
#                req.write('<span class="ok">[OK]</span><br/>\nDeleting record from stores ...')
#                
#                recordStore.begin_storing(session)
#                recordStore.delete_record(session, oldRec.id)
#                recordStore.commit_storing(session)
#                
#                dcRecordStore.begin_storing(session)
#                try: dcRecordStore.delete_record(session, rec.id)
#                except: pass
#                else: dcRecordStore.commit_storing(session)
#                req.write('<span class="ok">[OK]</span><br/>\n')
#                if len(rec.process_xpath(session, 'dsc')) and exists :
#                    # now the tricky bit - component records
#                    compStore.begin_storing(session)
#                    q = queryFactory.get_query(session, 'ead.parentid exact "%s/%s"' % (oldRec.recordStore, oldRec.id))
#                    req.write('Removing components...')
#                    rs = db.search(session, q)
#                    for r in rs:
#                        try:
#                            compRec = r.fetch_record(session)
#                        except (c3errors.FileDoesNotExistException, c3errors.ObjectDoesNotExistException):
#                            pass
#                        else:
#                            db.unindex_record(session, compRec)
#                            db.remove_record(session, compRec)
#                            compStore.delete_record(session, compRec.id)
#         
#                    compStore.commit_storing(session)
#                    req.write('<span class="ok">[OK]</span><br/>\n')
#            #add and index new record
#            req.write('indexing new record... ')
#            doc = ppFlow.process(session, StringDocument(xml))
#            rec = xmlp.process_document(session, doc)
#            assignDataIdFlow.process(session, rec)
#            
#            db.begin_indexing(session)
#            recordStore.begin_storing(session)
#            dcRecordStore.begin_storing(session)
#            
#            indexNewRecordFlow.process(session, rec)
#            
#            recordStore.commit_storing(session)
#            dcRecordStore.commit_storing(session)
#            
#            
#            if len(rec.process_xpath(session, 'dsc')):
#                compStore.begin_storing(session)
#                # extract and index components
#                compRecordFlow.process(session, rec)
#                compStore.commit_storing(session)
#                db.commit_indexing(session)
#                db.commit_metadata(session)
#                req.write('<span class="ok">[OK]</span><br/>\n')
#            else :
#                db.commit_indexing(session)
#                db.commit_metadata(session)   
#                req.write('<span class="ok">[OK]</span><br/>\n')
#            # write to file
#        if valid:
#            req.write('writing to file system... ')
#            filepath = os.path.join(sourceDir, filename)
#            pre = ''
#            if os.path.exists(filepath):
#                ws = re.compile('[\s]+')
#                xml = ws.sub(' ', read_file(filepath))
#                m = re.match('(.*?)<ead[>\s]', xml)
#                try :           
#                    pre = m.group(1)    
#                except:
#                    pass
#                os.remove(filepath)
#            try :
#                file = open(filepath, 'w')
#            except :
#                file = open(os.path.join(sourceDir,'%s.xml' % recid), 'w')
#            
#            tempRec = xmlp.process_document(session, orderTxr.process_record(session, rec))
#            indentTxr = db.get_object(session, 'indentingTxr')
#            file.write('%s\n%s' % (pre, indentTxr.process_record(session, tempRec).get_raw(session)))
#            file.flush()
#            file.close()    
#            editStore.delete_record(session, editRecid)
#            editStore.commit_storing(session)
#            req.write('<span class="ok">[OK]</span><br/>\n<p><a href="/ead/edit">Back to \'Editing Menu\'.</a></p>')
#            foot = self._get_genericHtml('footer.html')          
#            req.write('</div>' + foot)
#        return None               
#
# End of SUB-FORM FUNCTIONS     
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
            elif operation == 'test':
                self.test(session, req)
            elif operation == 'save':
                self.save(form)
            elif operation == 'refsubform':
                content = self.get_refForm(form)
                self.send_html(content, req)
            elif (operation == 'references'):
                content = self.get_fullRefs(session, form)
                self.send_xml(content, req)
                return
        else:
            content = self.show_editMenu()
            # send the display
            self.send_html(content, req)
    
rebuild = True
serv = None
session = None
db = None
db3 = None
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
    global session, serv, db, db3, qf, editStore, recordStore, authStore, formTxr, xmlp, indentingTxr, sourceDir
    
    session = Session()
    session.database = 'db_istc'
    session.environment = 'apache'
    session.user = None
    serv = SimpleServer(session, cheshirePath + '/cheshire3/configs/serverConfig.xml')
    db = serv.get_object(session, 'db_istc')
    db3 = serv.get_object(session, 'db_refs')
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