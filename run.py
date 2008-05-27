#!/home/cheshire/install/bin/python -i

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
            #print '[OK]'
        except UnicodeDecodeError:
            print '[Some indexes not built - non unicode characters!]'



        
        #try:
        #    rec = parser.process_document(session, doc)
        #except:
        #    print doc.get_raw(session)
        #    raise
        #recStore.create_record(session, rec)
        #db.add_record(session, rec)
        #db.index_record(session, rec)
        #if not x % 1000:
        #    print "%s in %s, %s/sec" % (x, time.time() - start, time.time() - start / x)


    db.commit_indexing(session)
    recordStore.commit_storing(session)
    db.commit_metadata(session)
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    print 'Indexing complete (%dh %dm %ds)' % (hours, mins, secs)



elif '-marc' in sys.argv:
    start = time.time()
    marcTxr = db.get_object(session, 'dataTransformer')
    formatTxr = db.get_object(session, 'indentingTxr')
    dir = '/home/cheshire/cheshire3/cheshire3/dbs/istc/data/'
    
    db.begin_indexing(session)
    recordStore.begin_storing(session)
    df.load(session, defpath + "/oldformdata/", codec='iso-8859-1')
    #t.encode('ascii', 'xmlcharrefreplace')
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

