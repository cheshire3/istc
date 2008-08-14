#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

import time, sys, os
osp = sys.path
sys.path = ["/home/cheshire/cheshire3/cheshire3/code"]
sys.path.extend(osp)
from www_utils import *
from baseObjects import Session
from server import SimpleServer
from document import StringDocument

import getpass
from crypt import crypt

#import psyco
#psyco.cannotcompile(lex.lex)
#psyco.cannotcompile(yacc.yacc)
#psyco.unbind(lex.lex)
#psyco.unbind(yacc.yacc)
#psyco.full()


# Build environment...
session = Session()
serv = SimpleServer(session, "/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
defpath = db.get_path(session, "defaultPath")
recordStore = db.get_object(session, 'recordStore')
sax = db.get_object(session, 'SaxParser')
authStore = db.get_object(session, 'istcAuthStore')

df = db.get_object(session, 'defaultDocumentFactory')
parser = db.get_object(session, 'LxmlParser')
app = db.get_object(session, 'AmpPreParser')


if ('-adduser' in sys.argv):
    un = raw_input('Please enter a username: ')
    if not un: inputError('You must enter a username for this user.')
    pw = getpass.getpass('Please enter a password for this user: ')
    if not (pw and len(pw)): inputError('You must enter a password for this user.')
    pw2 = getpass.getpass('Please re-enter the password to confirm: ')
    if pw != pw2: inputError('The two passwords submitted did not match. Please try again.')
    rn = raw_input('Real name of this user (not mandatory): ')
    addy = raw_input('Email address for this user (not mandatory): ')
    xml = read_file('xsl/admin.xml').replace('%USERNAME%', un)
    for k,v in {'%password%': crypt(pw, pw[:2]), '%realName%': rn, '%email%': addy}.iteritems():
        if v and len(v):
            xml = xml.replace(k, '\n  <%s>%s</%s>' % (k[1:-1],v,k[1:-1]))
        else:
            xml = xml.replace(k, '')
    doc = StringDocument(xml)
    rec = parser.process_document(session, doc)
    id = rec.process_xpath(session, '/config/@id')[0]
    rec.id = id
    authStore.store_record(session, rec)
    authStore.commit_storing(session)
    try:
        user = authStore.fetch_object(session, id)
    except c3errors.FileDoesNotExistException:
        print 'ERROR: User not successfully created. Please try again.'
    else:
        print 'OK: Username and passwords set for this user'
    #print user
    sys.exit()  
       
if '-test' in sys.argv:
    from PyZ3950.CQLParser import parse as ps
    q = ps('c3.idx-ISTC-number any "ia*"')
    rs = db.search(session, q)
    sys.exit()

elif '-load' in sys.argv:
    start = time.time()
    flow = db.get_object(session, 'buildIndexWorkflow')


    
    db.begin_indexing(session)
    recordStore.begin_storing(session)
   # df.load(session, defpath + "/data/", codec='iso-8859-1')
    df.load(session, defpath + "/data/", codec='utf-8')
    print 'Loading'
    x = 0
    a = 0
    for doc in df:    
        x += 1
        
        doc = app.process_document(session, doc)
        try:
            rec = parser.process_document(session, doc)
        except:
            print doc.get_raw(session)
            a = a+1
            continue
        
        recordStore.create_record(session, rec)
        
        db.add_record(session, rec)

    
    #try:
    #flow.process(session, df)
    #except:
    #    print "error"
    print a
    x = 0
    print "Indexing records..."
    for rec in recordStore:    
        x += 1
        #print x
        try:
            db.index_record(session, rec)
            print '[OK]'
        except UnicodeDecodeError:
            print '[Some indexes not built - non unicode characters!]'



        
#        try:
#            rec = parser.process_document(session, doc)
#        except:
#            print doc.get_raw(session)
#            raise
#        recStore.create_record(session, rec)
#        db.add_record(session, rec)
#        db.index_record(session, rec)
#        if not x % 1000:
#            print "%s in %s, %s/sec" % (x, time.time() - start, time.time() - start / x)


    db.commit_indexing(session)
    recordStore.commit_storing(session)
    db.commit_metadata(session)
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    print 'Indexing complete (%dh %dm %ds)' % (hours, mins, secs)


elif '-extractTest' in sys.argv:
    
    def _process_tagName(tagname):
        for i, c in enumerate(tagname):
            if c != '0':
                return int(tagname[i:])
    
    def process_record(session, rec):
        fields = {}
        tree = rec.get_dom(session)
        try:
            walker = tree.getiterator("controlfield")
        except AttributeError:
            # lxml 1.3 or later
            walker = tree.iter("controlfield")  
        for element in walker:
            tag = _process_tagName(element.get('tag'))
            contents = element.text
            if fields.has_key(tag):
                fields[tag].append(contents)
            else:
                fields[tag] = [contents]
                
        try:
            walker = tree.getiterator("datafield")
        except AttributeError:
            # lxml 1.3 or later
            walker = tree.iter("datafield")  
        for element in walker:
            tag = _process_tagName(element.get('tag'))
            try:
                children = element.getiterator('subfield')
            except AttributeError:
                # lxml 1.3 or later
                walker = element.iter('subfield') 
            subelements = [(c.get('code'), c.text) for c in children]
            contents = (element.get('ind1'), element.get('ind2'), subelements)         
            if fields.has_key(tag):
                fields[tag].append(contents)
            else:
                fields[tag] = [contents] 
        leader = tree.xpath('//leader')[0]
        l = leader.text
        fields[0] = [''.join([l[5:9], l[17:20]])]
        print fields
        return fields
    

elif '-marc' in sys.argv:
    start = time.time()
    marcTxr = db.get_object(session, 'dataTransformer')
    formatTxr = db.get_object(session, 'indentingTxr')
    dir = '/home/cheshire/cheshire3/cheshire3/dbs/istc/dataprep/testFormat/'
    
    db.begin_indexing(session)
    recordStore.begin_storing(session)
    #df.load(session, defpath + "/dataprep/test/", codec='utf-8')
    df.load(session, defpath + "/dataprep/test/", codec='iso-8859-1')
    #t.encode('ascii', 'xmlcharrefreplace')
    #print 'Loading'
    x = 0
    a = 0
    for doc in df:    
        x += 1
        
        doc = app.process_document(session, doc)
        try:
            rec = parser.process_document(session, doc)
        except:
            print doc.get_raw(session)
            a = a+1
            break
            
        d2 = marcTxr.process_record(session, rec)
        rec = parser.process_document(session, d2)
        filename = rec.process_xpath(session, '//controlfield[@tag="001"]/text()')[0]
        print filename
    
        d3 = formatTxr.process_record(session, rec)
               
        filepath = os.path.join(dir, '%s.xml' % filename)
        if os.path.exists(filepath):
            print 'file exists at %s' % filepath
        else:
            
            file = open(filepath, 'w', 0)
            file.write(d3.get_raw(session))
            file.close 

    print a
    
elif '-testKeys' in sys.argv:
    session.database = 'db_usa'
    db_usa = serv.get_object(session, 'db_usa')
    idx = db_usa.get_object(session, 'idx-usa-code')
    refs = []
    for i in idx:
        refs.append(i.queryTerm)
   # print refs
    usaRefs = []
    for rec in recordStore:
        temp = rec.process_xpath(session, "//datafield[@tag='952']/subfield[@code='a']/text()")
        if len(temp):
            for t in temp:
                if t.find(' ') == -1:
                    usaRefs.append(t.lower())
                else:    
                    usaRefs.append(t[:t.find(' ')].lower())
    usaSet = set(usaRefs)
    errors = 0
    for item in usaSet:
        if item in refs:
            pass
        else :
            errors += 1
            print item 
    print errors
    print 'end'   
            
        

        