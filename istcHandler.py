
import sys, os, cgitb, time, re, smtplib

from mod_python import apache, Cookie
from mod_python.util import FieldStorage

sys.path.insert(1,'/home/cheshire/cheshire3/cheshire3/code')

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session
from cheshire3.utils import flattenTexts
from cheshire3.document import StringDocument
from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from istcLocalConfig import *
from lxml import etree
from cheshire3.cqlParser import Triple

import urllib

class istcHandler:
    templatePath = "/home/cheshire/cheshire3/cheshire3/www/istc/html/template.html"
    rtfPath = "/home/cheshire/cheshire3/cheshire3/www/istc/outputTemplate.txt"
    printPath = "/home/cheshire/cheshire3/cheshire3/www/istc/html/printTemplate.html"

    def __init__(self, lgr):
        self.logger = lgr



    def send_html(self, data, req, code=200):
        req.content_type = 'text/html; charset=utf-8'
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()
        
        
    def send_txt(self, data, req, code=200):
        #req.content_type = 'application/msword; charset=utf-8'
        req.content_type = 'application/msword'
        req.content_length = len(data)
        req.send_http_header()
        #raise ValueError(data)
       # if (type(data) == unicode):
       #     raise ValueError(type)
       #     data = data.encode('utf-8')
        req.write(data)
        req.flush()


    def send_xml(self, data, req, code=200):
        req.content_type = 'text/xml'
        req.content_length = len(data)
        req.send_http_header()
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()       
    #- end send_xml()


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
	
        return qString



    def _cleverTitleCase(self, txt):
        global stopwords
        words = txt.split()
        for x in range(len(words)):
            if (x == 0 and not words[x][0].isdigit()) or (words[x][0].isalpha()) and (words[x]):
                words[x] = words[x].title()
        return ' '.join(words)
    

    def sort_resultSet(self, session, rs, form):
        session.database = db.id
           
        try:
            sort = form.get('sort', None).value               
        except:
            sort = 'idx-title'
            
        indexes = sort.split(',')
        for idxstr in indexes:
            bits = idxstr.split('|')
            idx = db.get_object(session, bits[0])
            if len(bits) > 1:
                up = int(bits[1] == 'up')                        
            else:
                up = 1
            rs.order(session, idx, ascending=up, missing=[-1,1][up])
        rss.delete_resultSet(session, rs.id)
        rss.store_resultSet(session, rs)
        return rs


    def handle_istc(self, session, form):
        self.logger.log('entering handle_istc')
        pagesize = 20
        start = 0
        
        session.database = db.id
        
        locations = form.get('locations', 'all')
        if not locations == 'all':
            locString = '&locations=%s' % locations
        else:
            locString = ''

        
        html = []
        
        if not (form.has_key('rsid')):
            
            cql = self.generate_query(form)
            try:
                q = qf.get_query(session, cql.encode('utf-8'))
                self.logger.log(q)
            except:
                return ('Search Error', '<p>Could not parse your query. <a href="http://istc.cheshire3.org">Please try again</a>. %s' % cql, '')
            
            try:
                rs = db.search(session, q)     
            except:
                return ('Search Error', '<p>Could not complete your query. <a href="http://istc.cheshire3.org">Please try again</a>. %s' % cql, '')
            
            

            try:
                rsid = rss.create_resultSet(session, rs)
                rs.id = rsid
            except:
                raise
            
            cqlStr = self._interpret_query(q, [], [])          
            html.append("<strong>Your search was for %s </strong><br/><br/>" % cqlStr)
        
        else:
            try:
                rsid = form.get('rsid', None).value
            except:
                # should never happen?
                return ('An Error has Occurred', '<p>Could not parse your query. <a href="http://istc.cheshire3.org">Please try again</a> %s' % cql, '')
                
            start = int(form.get('start', 0))
            try :
                rs = rss.fetch_resultSet(session, rsid)
            except:
                raise           
            
        hits = len(rs)
        if hits:
            menubits = []
            
            if (form.has_key('sort')):
                rs = self.sort_resultSet(session, rs, form)
                

            if start > 0 and start+pagesize < len(rs):
                navString = '<a href="/istc/search/search.html?operation=search&rsid=%s&start=%d%s">Previous</a>&nbsp;|&nbsp;<a href="/istc/search/search.html?operation=search&rsid=%s&start=%d%s">Next</a>' % (rsid, start-pagesize, locString, rsid, start+pagesize, locString)
            elif start > 0 and start+pagesize >= len(rs):
                navString = '<a href="/istc/search/search.html?operation=search&rsid=%s&start=%d%s">Previous</a>&nbsp;|&nbsp;Next' % (rsid, start-pagesize, locString)
            elif start == 0 and start+pagesize < len(rs):
                navString = 'Previous&nbsp;|&nbsp;<a href="/istc/search/search.html?operation=search&rsid=%s&start=%d%s">Next</a>' % (rsid, start+pagesize, locString)
            else :
                navString = ''

            html.append(navString)
                
            html.append('<h1>%d Results</h1><p>Sort by <a href="/istc/search/search.html?operation=search&rsid=%s&sort=idx-author%s">Author </a>, <a href="/istc/search/search.html?operation=search&rsid=%s&sort=idx-title%s">Title </a> or <a href="/istc/search/search.html?operation=search&rsid=%s&sort=idx-publoc%s">Place of Publication</a><br/><br/>' % (hits, rsid, locString, rsid, locString, rsid, locString))

            for i in range(start, min(start+pagesize, len(rs))):

                rec = recStore.fetch_record(session, rs[i].id)
                
                html.append('%d. ' %  (i+1))                
                html.append('<input type="checkbox" name="recSelect" value="%s"/>' % i)
                
                try:
                    elms = rec.process_xpath(session, '//datafield[@tag="245"]/subfield[@code="a"]')
                    title = flattenTexts(elms[0])

                except:
                    raise
                    try:
                        elms = rec.process_xpath(session, '//datafield[@tag="130"]/subfield[@code="a"]')
                        title = flattenTexts(elms[0])
                    except:
                        title = ""
                        
                try:
                    elms = rec.process_xpath(session, '//datafield[@tag="100"]/subfield[@code="a"]')
                    author = flattenTexts(elms[0])
                except:
                    try:
                        elms = rec.process_xpath(session, '//datafield[@tag="100"]')
                        author = flattenTexts(elms[0])
                    except:
                        author = ""
                try:
                    elms = rec.process_xpath(session, '//datafield[@tag="260"]/subfield[@code="b"]')
                    imprint = "- %s" % flattenTexts(elms[0])

                except:
                    imprint = ""
                try:
                    elms = rec.process_xpath(session, '//datafield[@tag="260"]/subfield[@code="c"]')
                    date = flattenTexts(elms[0])
                except:
                    date= ""
          
                html.append('<a href="/istc/search?operation=record&rsid=%s&q=%s%s">%s</a><br/>&nbsp;&nbsp;&nbsp;%s %s %s <br/><br/>' % (rsid, i, locString, title, author, imprint, date))       
            
            menubits.extend(['<div class="menugrp">',
                            '<div class="menuitem"><a href="#" onclick="submitForm(\'print\')">Print Selected<img src="/istc/images/link_print.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div><br />',
                            '<div class="menuitem"><a href="#" onclick="submitForm(\'email\')">Email Selected<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div><br />',
                            '<div class="menuitem"><a href="#"  onclick="submitForm(\'save\')">Save Selected<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div><br />',
                            '<div class="menuitem">with expanded bibliographical refs <input type="checkbox" id="expandedbib"/></div>',
                            '</div>'])
            
            
            if hits <= 200:
                menubits.extend(['<div class="menugrp">',
                            '<div class="menuitem"><a href="/istc/search?operation=print&rsid=%s%s">Print all Records<img src="/istc/images/link_print.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div><br />' % (rsid, locString),
                            '<div class="menuitem"><a href="/istc/search?operation=email&rsid=%s%s">Email all Records<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div><br />' % (rsid, locString),
                            '<div class="menuitem"><a href="/istc/search?operation=save&rsid=%s%s">Save all Records<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></a></div>' % (rsid, locString),
                            '</div>'])
            
            
        else:
            html.append("There are no records that match your query.  (%s)" % cql.decode('utf-8'))
            menubits = []
        
        if not locations == 'all':
            return ('Search Results', '<form id="mainform" action="/istc/search" method="get"><input type="hidden" name="rsid" value="%s" /><input type="hidden" name="type" value="selected" /><input type="hidden" id="opvalue" name="operation" value="print" /><input type="hidden" id="expand" name="expand" value="false" /><input type="hidden" name="locations" value="%s" />%s</form>' % (rsid, locations, ''.join(html)), ''.join(menubits))
        else :
            return ('Search Results', '<form id="mainform" action="/istc/search" method="get"><input type="hidden" name="rsid" value="%s" /><input type="hidden" name="type" value="selected" /><input type="hidden" id="opvalue" name="operation" value="print" /><input type="hidden" id="expand" name="expand" value="false" />%s</form>' % (rsid, ''.join(html)), ''.join(menubits))


    def _interpret_query(self, cql, stack = [], string = []):    

        if self._has_operand(cql, 'left'):           
            new = cql.leftOperand
            cql.leftOperand = None
            stack.append(cql)
            return self._interpret_query(new, stack, string)
        elif self._has_boolean(cql):
            string.append('%s' % cql.boolean.value)
            cql.boolean.value = None
            return self._interpret_query(cql, stack, string)
        elif self._has_operand(cql, 'right'):            
            new = cql.rightOperand
            cql.rightOperand = None
            stack.append(cql)
            return self._interpret_query(new, stack, string)
        else :
            if not isinstance(cql, Triple):    
                substring = [] 
                index = idxNames['%s' % cql.index.value]
                substring.append(index)
                substring.append('%s' % cql.relation.value)  
    
                substring.append("\"%s\"" % cql.term.value)
            
                if len(substring):
                    string.extend(['(', ' '.join(substring), ')'])
            if len(stack):
                return self._interpret_query(stack.pop(), stack, string)
            else :
                return ' '.join(string)


    def _has_boolean(self, clause):
        try:
            clause.boolean.value
        except:
            return False
        else:
            if clause.boolean.value == None:
                return False
            else:
                return True
        
            

    def _has_operand(self, clause, side):
        if side == 'left':
            try:
                clause.leftOperand
            except:
                return False
            else :
                if clause.leftOperand == None:
                    return False
                else :
                    return True
        elif side == 'right':
            try:
                clause.rightOperand
            except:
                return False
            else :
                if clause.rightOperand == None:
                    return False
                else :
                    return True


      

    def display_rec(self, session, form):
        session.database = 'db_istc'
        txr = db.get_object(session, 'recordTxr-screen')
        menuTxr = db.get_object(session, 'menuTxr')
        rsid = int(form['rsid'].value)
        id = int(form['q'].value)
        locations = form.get('locations', 'all')
        
        if not locations == 'all':
            locString = '&locations=%s' % locations
        else :
            locString = ''

            
        rs = rss.fetch_resultSet(session, rsid)
        
        if id > 0 and id < len(rs)-1:
            navstring = '<a href="/istc/search/search.html?operation=record&rsid=%s&q=%d%s">Previous</a>&nbsp;|&nbsp;<a href="/istc/search/search.html?operation=record&rsid=%s&q=%d%s">Next</a>' % (rsid, id-1, locString, rsid, id+1, locString)
        elif id > 0 and id < len(rs):
            navstring = '<a href="/istc/search/search.html?operation=record&rsid=%s&q=%d%s">Previous</a>&nbsp;|&nbsp;Next' % (rsid, id-1, locString)
        elif id == 0 and id < len(rs)-1:
            navstring = 'Previous&nbsp;|&nbsp;<a href="/istc/search/search.html?operation=record&rsid=%s&q=%d%s">Next</a>' % (rsid, id+1, locString)
        else:
            navstring = ''

        if len(rs):
            rec = rs[id].fetch_record(session)           
            #create extra bits for navigation menu            
            menu = menuTxr.process_record(session, rec)
            doc = self._transform_record(rec, txr, 'false', locations)
            return ('Record Details', doc.replace('%nav%', navstring), menu.get_raw(session))
        else:
            raise ValueError(id)
            
            
    def get_fullRefs(self, session, form):
        ref = form.get('q', None)
        ref = ref.replace('*', '\*')
        session.database = db3.id
        q = qf.get_query(session, 'c3.idx-refs-code exact "%s"' % (ref))
        rs = db3.search(session, q)
        if len(rs):
            recRefs = rs[0].fetch_record(session).get_xml(session)
        else :
            while ref.rfind(' ') != -1 and not len(rs):
                ref = ref[:ref.rfind(' ')].strip()
                q.term.value = ref.decode('utf-8')
                rs = db3.search(session, q)
            if len(rs):
                recRefs = rs[0].fetch_record(session).get_xml(session)
            else:
                recRefs = '<record></record>' 
        return recRefs
        
        
    def get_usaRefs(self, session, form):
        ref = form.get('q', None)
        session.database = db2.id
        q = qf.get_query(session, 'c3.idx-usa-code exact "%s"' % (ref.split(' ')[0].strip()))
        rs = db2.search(session, q)
        if len(rs):
            recRefs = rs[0].fetch_record(session).get_xml(session)
        else :
            while ref.rfind(' ') != -1 and not len(rs):
                ref = ref[:ref.rfind(' ')].strip()
                q.term.value = ref.decode('utf-8')
                rs = db2.search(session, q)
            if len(rs):
                recRefs = rs[0].fetch_record(session).get_xml(session)
            else:
                recRefs = '<record></record>'
        return recRefs     
        
    def get_format(self, session, form):
        string = form.get('q', None)
        return '<output>%s</output>' % string.replace('4~~', '<main>4</main><sup>to</sup>').replace('8~~', '<main>8</main><sup>vo</sup>').replace('f~~', '<main>f</main><sup>o</sup>').replace('bdsde', 'Broadside').replace('Bdsde', 'Broadside').replace('~~', '<sup>mo</sup>')
    
    def printRecs(self, form):
        istc = form.get('istc', None)
        txr = db.get_object(session, 'recordTxr-print')
        f = file(self.printPath)
        tmpl = f.read()
        f.close()
        expand = form.get('expand', 'false') 
        locations = form.get('locations', 'all')
        if istc:
            session.database = 'db_istc'
            q = qf.get_query(session, 'dc.identifier exact "%s"' % (istc.value))
            rs = db.search(session, q)
            if len(rs):
                rec = rs[0].fetch_record(session)                
                return tmpl.replace('%%%CONTENT%%%',  self._transform_record(rec, txr, expand, locations))
        else:    
            type = form.get('type', 'all') 
            rsid = form.get('rsid', None)
            recs = form.getlist('recSelect')             
            if rsid:    
                rs = rss.fetch_resultSet(session, rsid.value)
                output = []
                if type == 'all':                   
                    for r in rs:
                        rec = r.fetch_record(session)
                        output.append(self._transform_record(rec, txr, expand, locations))
                else:
                    if len(recs):
                        for r in recs:
                            rec = rs[int(r)].fetch_record(session)
                            output.append(self._transform_record(rec, txr, expand, locations))
                    
                return tmpl.replace('%%%CONTENT%%%',  '<br/>------------<br/>'.join(output))
         
    
    def saveRecs(self, form):
        istc = form.get('istc', None)
        txr = db.get_object(session, 'recordTxr-save')
        f = file(self.rtfPath)
        tmpl = f.read()
        f.close()
        expand = form.get('expand', 'false')
        locations = form.get('locations', 'all')
        if istc:
            session.database = 'db_istc'
            q = qf.get_query(session, 'dc.identifier exact "%s"' % (istc.value))
            rs = db.search(session, q)
            if len(rs):
                rec = rs[0].fetch_record(session)
                output = [self._transform_record(rec, txr, expand, locations)]
        else:           
            type = form.get('type', 'all') 
            rsid = form.get('rsid', None)
            recs = form.getlist('recSelect')            
            if rsid:
                rs = rss.fetch_resultSet(session, rsid.value)
                output = []
                if type == 'all':
                    for r in rs:
                        rec = r.fetch_record(session)
                        output.append(self._transform_record(rec, txr, expand, locations))
                else:
                    if len(recs):
                        for r in recs:
                            rec = rs[int(r)].fetch_record(session)
                            output.append(self._transform_record(rec, txr, expand, locations))
                            
        return  tmpl.replace('%%%DATA%%%', self._RTFify(''.join(output)))


    def _RTFify(self, string):
         ucre = re.compile('&#([0-9]+);')
         newString = re.sub (ucre, '\u\\1?', string)
         newString = newString.replace('&amp;', '&')
         return newString

    
    def send_email(self, address=None, rsid=None, istc=None, type=None, recs=[], expand='false', locations='all'):
        txr = db.get_object(session, 'recordTxr-email')
        f = file(self.rtfPath)
        tmpl = f.read()
        f.close()
        if istc:
            session.database = 'db_istc'
            q = qf.get_query(session, 'dc.identifier exact "%s"' % (istc.value))
            rs = db.search(session, q)
            if len(rs):
                rec = rs[0].fetch_record(session)
                output = [self._transform_record(rec, txr, expand, locations)]
        else:                      
            if rsid:
                rs = rss.fetch_resultSet(session, rsid.value)
                output = []
                if type == 'all':
                    for r in rs:
                        rec = r.fetch_record(session)
                        output.append(self._transform_record(rec, txr, expand, locations))
                else:
                    if len(recs):
                        for r in recs:
                            rec = rs[int(r)].fetch_record(session)
                            output.append(self._transform_record(rec, txr, expand, locations))
                                   
        message = MIMEMultipart()
        message['From'] = 'istc@localhost'
        message['To'] = address
        message['Subject'] = 'ISTC Records'
        message.attach(MIMEText('The records you requested are attached.'))
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload( tmpl.replace('%%%DATA%%%', self._RTFify(''.join(output))))
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="ISTCrecords.rtf"')
        message.attach(part)
        
        smtp = smtplib.SMTP()
        smtp.connect(host='mail1.liv.ac.uk', port=25)
        smtp.sendmail('istc@localhost', address, message.as_string())
        smtp.close()
        return ('result', 'File emailed successfully', '')
        
    
    def emailRecs(self, form):
        istc = form.get('istc', None)
        address = form.get('address', None)        
        type = form.get('type', 'all')
        rsid = form.get('rsid', None)
        recs = form.getlist('recSelect')
        expand = form.get('expand', 'false')
        locations = form.get('locations', 'all')
        if not address:
            repl = []
            if istc:
                repl.extend(['<input type="hidden" name="istc" value="%s"/>' % istc,
                             '<input type="hidden" name="expand" value="%s"/>' % expand,
                             '<input type="hidden" name="locations" value="%s"/>' % locations])
            else:
                repl.extend(['<input type="hidden" name="rsid" value="%s"/>' % rsid,
                             '<input type="hidden" name="type" value="%s"/>' % type,
                             '<input type="hidden" name="expand" value="%s"/>' % expand,
                             '<input type="hidden" name="locations" value="%s"/>' % locations])
                for rec in recs:
                    repl.append('<input type="hidden" name="recSelect" value="%s"/>' % rec)
            f = read_file('email.html')
            f = f.replace('%Details%', ''.join(repl))
            return ('Email Request', f, '')
        else:
            if istc:
                return self.send_email(istc=istc, address=address, expand=expand, locations=locations)
            elif rsid and type == 'all':
                return self.send_email(rsid=rsid, type=type, address=address, locations=locations)
            else :
                return self.send_email(rsid=rsid, type=type, address=address, recs=recs, expand=expand, locations=locations)

                         
    def _transform_record(self, rec, txr, expand, locations):
        dom = rec.get_dom(session)
        txr.txr = etree.XSLT(txr.parsedXslt)
        if not txr.params:
            txr.params = {}
        txr.params['expand'] = '"%s"' % expand
        txr.params['locations'] = '"%s"' % locations                            
        result = txr.txr(dom, **txr.params)
        return StringDocument(str(result)).get_raw(session)


    def browse(self, form):
        idx = form.get('fieldidx1', None)
        rel = form.get('fieldrel1', 'exact')
        if idx == 'bib.originPlace':
            rel = 'all'
        scanTerm = form.get('fieldcont1', '')
        firstrec = int(form.get('firstrec', 1))
        numreq = int(form.get('numreq', 25))
        rp = int(form.get('responsePosition', 4))
        qString = '%s %s "%s"' % (idx, rel, scanTerm)
        t = []

        db = serv.get_object(session, 'db_istc')
        try:
            scanClause = qf.get_query(session, qString)          
        except:
            qString = self.generate_query(form)
            try:
                scanClause = qf.get_query(session, qString)      
            except:
                t.append('Unparsable query: %s' % qString)
                return (" ".join(t), '<p>An invalid query was submitted.</p>')
            
        t.append('Browse Indexes')

        hitstart = False
        hitend = False
        #scanData = db.scan(session, scanClause, 5, direction="<=")
        if (scanTerm == ''):
            hitstart = True
            rp = 0
        if (rp == 0):
            scanData = db.scan(session, scanClause, numreq, direction=">")
            if (len(scanData) < numreq): hitend = True
        elif (rp == 1):
            scanData = db.scan(session, scanClause, numreq, direction=">=")
            if (len(scanData) < numreq): hitend = True
        elif (rp == numreq):
            scanData = db.scan(session, scanClause, numreq, direction="<=")
            scanData.reverse()
            if (len(scanData) < numreq): hitstart = True
        elif (rp == numreq+1):
            scanData = db.scan(session, scanClause, numreq, direction="<")
            scanData.reverse()
            if (len(scanData) < numreq): hitstart = True
            elif len(scanData[0]) == 3: hitstart = True
        else:
            
            nFwd = numreq - rp
            nBack = rp
            # Need to go down...
            try:
                scanData = db.scan(session, scanClause, nBack, direction="<=")
            except:
                
                scanData = []
                # ... then up
            try:
                scanData1 = db.scan(session, scanClause, nFwd, direction=">=")
            except:
                scanData1 = []
            
            
            if (len(scanData1) < nFwd):
                hitend = True
            if (len(scanData) < nBack):
                hitstart = True
            # try to stick them together
            try:
                if scanData1[0][0] == scanData[0][0]:
                    scanData = scanData[1:]
                else:
                    scanData.insert(0, None)
                    scanData1[:-1]
            except:
                 pass

            scanData.reverse()
            scanData.extend(scanData1)
            del scanData1
 
        totalTerms = len(scanData)

        if (totalTerms > 0):
            t.append('Results')
            rows = ['<table width = "90%" cellspacing="5" summary="list of terms in this index">',
                    '<tr class="headrow"><td>Term</td><td>Records</td></tr>']

            rowCount = 0
            
            if (hitstart):
                rows.append('<tr class="odd"><td colspan="2">-- start of index --</td></tr>')
                rowCount += 1
                prevlink = ''
            else:
                prevlink=""
                prevlink = '<a href="/istc/search/%s?operation=scan&amp;fieldidx1=%s&amp;fieldrel1=%s&amp;fieldcont1=%s&amp;responsePosition=%d&amp;numreq=%d"><!-- img -->Previous %d terms</a>' % (script, idx, rel, cgi_encode(scanData[0][0]), numreq, numreq, numreq)
                 
 
            
            dodgyTerms = []
            for i in range(len(scanData)):
                item = scanData[i]
                try :
                    term = item[0]
                except :
                    row="""
         <tr class="notfound">
          <td align="center" colspan="2">
            [ Your Term Would be Here ]
          </td>
        </tr>"""
                    rows.append(row)
                    continue
                try: term.encode('utf-8', 'latin-1')
                except: continue
                if not term:
                    continue

                # TODO: ideally get original, un-normalised version from index
                # until then do a clever version of term.title()
                if (idx not in ['dc.identifier']):
                    displayTerm = self._cleverTitleCase(term)
                else:
                    displayTerm = term

                
                if (term.lower() == scanTerm.lower()):
                    displayTerm = '<strong>%s</strong>' % displayTerm
                    
                rowCount += 1                   
                if (rowCount % 2 == 1): rowclass = 'odd';
                else: rowclass = 'even';
               
                row = """
         <tr class="%ROWCLASS%">
          <td align="left">
            <a href="SCRIPT?operation=search&amp;fieldidx1=%IDX%&amp;fieldrel1=%REL%&amp;fieldcont1=%CGITERM%&frombrowse=true" title="Find matching records" class="termLink">%TERM%</a>
          </td>
          <td class="hitCount" align="right">%COUNT%</td>
        </tr>"""     
           
              #  row = browse_result_row
                paramDict =  {
                    '%ROWCLASS%': rowclass,
                    '%IDX%': idx, 
                    '%REL%': rel, 
                    '%CGITERM%': cgi_encode(term), 
                    '%TERM%': displayTerm, 
                    '%COUNT%': str(item[1][1]),
                    'SCRIPT': "search.html"
                }
                for key, val in paramDict.iteritems():
                    row = row.replace(key, val)

                rows.append(row)

            #- end for each item in scanData
           
            if (hitend):
                rowCount += 1
                if (rowCount % 2 == 1): rowclass = 'odd';
                else: rowclass = 'even';
                rows.append('<tr class="%s"><td colspan="2">-- end of index --</td></tr>' % (rowclass))
                nextlink = 'next %d terms' % numreq
            else:
                nextlink = '<a href="/istc/search/%s?operation=scan&amp;fieldidx1=%s&amp;fieldrel1=%s&amp;fieldcont1=%s&amp;responsePosition=%d&amp;numreq=%d"><!-- img -->Next %d terms</a>' % (script, idx, rel, cgi_encode(scanData[-1][0]), 0, numreq, numreq)

            del scanData
            rows.append('</table>')           
            rows.extend(['<div class="scannav"><p>%s</p></div>' % (' | '.join([prevlink, nextlink])),
                         '</div><!-- end of single div -->',
                         '</div> <!-- end of wrapper div -->'
                         ])
            #- end hit navigation
            
            return (" ".join(t),'\n'.join(rows))

        else:
            t.append('Error')
            return (" ".join(t), '<p class="error">No terms retrieved from index. You may be browsing outside the range of terms within the index.</p>')

##     #- end browse() ------------------------------------------------------------
    
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
        if operation :
            if (operation == 'record'):
                (t, d, e) = self.display_rec(session, form)
            elif (operation == 'search'):
                (t, d, e) = self.handle_istc(session, form)
            elif (operation == 'scan'):
                (t, d) = self.browse(form)
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
            elif (operation == 'references'):
                self.logger.log('getting refs')
                content = self.get_fullRefs(session, form)
                self.send_xml(content, req)
                return
            elif (operation == 'usareferences'):
                content = self.get_usaRefs(session, form)
                self.send_xml(content, req)
                return
            elif (operation == 'format'):
                content = self.get_format(session, form)
                self.send_xml(content, req)
                return
        else:       
            if (path == 'browse.html'):              
                f = file('browse.html')
                t = "Browse"
            else:       
                f= file("index.html")
                t = "Search"
            d = f.read()
            f.close()
            
            
#        path = req.uri[1:] 
#        path = path[path.rfind('/')+1:]
#
#        e = ""
#        if (path =="list.html"):
#	        (t, d) = self.handle_list(session, form)           
#        elif (path == "search.html"):
#            cql = self.generate_query(form)
#            (t, d) = self.handle_istc(session, cql)
#        elif (path == "record.html"):
#            (t, d) = self.display_rec(session, form)
#        elif (path  == 'scan.html'):
#            (t, d) = self.browse(form)   
#        else:            
#            if (os.path.exists(path)):
#                f = file(path)
#                d = f.read()
#                f.close()
#                stuff = d.split("\n", 1)
#                if (len(stuff) == 1):
#                    t = "Cheshire/ISTC"
#                else:
#                    t = stuff[0]
#                    d = stuff[1]
#            else:
#                                
#                f= file("index.html")
#                d = f.read()
#                f.close()
#                t = "Search"
#  
            
        extra = '' #TODO check if this is needed - not sure %EXTRA% ever exists
 #       raise ValueError(d)
 #       d = d.encode('utf8')
 #       d = d.replace('iso-8859-1', 'utf-8')
 #       e = e.encode('utf8')
        tmpl = tmpl.replace("%CONTENT%", d)
        tmpl = tmpl.replace("%CONTENTTITLE%", t)
        tmpl = tmpl.replace("%EXTRA%", extra)
        tmpl = tmpl.replace("%EXTRATABLESTUFF%", e)
	self.send_html(tmpl, req)


    
os.chdir("/home/cheshire/cheshire3/cheshire3/code")

from cheshire3.baseObjects import Session
session = Session()
serv = SimpleServer(session, '/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml')



db = serv.get_object(session, 'db_istc')
db2 = serv.get_object(session, 'db_usa')
db3 = serv.get_object(session, 'db_refs')

session.database = db.id
dfp = db.get_path(session, "defaultPath")
recStore = db.get_object(session, 'recordStore')
indexStore = db.get_object(session, 'indexStore')
rss = db.get_object(session, 'resultSetStore')
usaRecStore = db2.get_object(session, 'usaRecordStore')
usaIndexStore = db2.get_object(session, 'usaIndexStore')
refsRecStore = db3.get_object(session, 'refsRecordStore')
refsIndexStore = db3.get_object(session, 'refsIndexStore')

qf = db.get_object(session, 'baseQueryFactory')

idxNames = {"anywhere": 'General Keywords',
            "creator":'Author',
            "title":'Title',
            "originplace":'Location of Print',
            "publisher":'Printer',
            "identifier":'ISTC Number',
            "format":'Format',
            "posessinginstitution":'Location',
            "year":'Start or exact Year (008)',
            "date":'Publication Date',
            "language":'Language',
            "blshelfmark":'BL Shelfmark'
                }

logfilepath = '/home/cheshire/cheshire3/cheshire3/www/istc/logs/searchhandler.log'
#from cheshire3.web.www_utils import FileLogger



def handler(req):
    # do stuff
    os.chdir("/home/cheshire/cheshire3/cheshire3/www/istc/html/")
    remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)                   # get the remote host's IP for logging
    lgr = FileLogger(logfilepath, remote_host)                                  # initialise logger object
    istchandler = istcHandler(lgr)        
    try:
        istchandler.handle(req)
        try: lgr.flush()                                                        # flush all logged strings to disk
        except: pass
    except:
        req.content_type = "text/html; charset=utf-8"
        cgitb.Hook(file = req).handle()
    return apache.OK

