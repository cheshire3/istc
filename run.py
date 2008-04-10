#!/home/cheshire/install/bin/python -i

import time, sys, os
osp = sys.path
sys.path = ["/home/cheshire/cheshire3/cheshire3/code"]
sys.path.extend(osp)

from baseObjects import Session
from server import SimpleServer
from document import StringDocument
from PyZ3950 import CQLParser
import c3errors
import lex, yacc
import random

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


df = db.get_object(session, 'defaultDocumentFactory')
parser = db.get_object(session, 'LxmlParser')
app = db.get_object(session, 'AmpPreParser')
    
       
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
    df.load(session, defpath + "/data/", codec='iso-8859-1')
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
