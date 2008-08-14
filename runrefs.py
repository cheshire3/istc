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




# Build environment...
session = Session()
serv = SimpleServer(session, "/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml")

session.database = 'db_refs'
db = serv.get_object(session, 'db_refs')
defpath = db.get_path(session, "defaultPath")
recordStore = db.get_object(session, 'refsRecordStore')
sax = db.get_object(session, 'SaxParser')


df = db.get_object(session, 'defaultDocumentFactory')
parser = db.get_object(session, 'LxmlParser')
app = db.get_object(session, 'AmpPreParser')
    
       


if '-load' in sys.argv:
    start = time.time()
    #flow = db.get_object(session, 'buildIndexWorkflow')


    
    db.begin_indexing(session)
    recordStore.begin_storing(session)
    #df.load(session, defpath + "/refsData/", codec='iso-8859-1', tagName='record')
    df.load(session, defpath + "/refsData/", codec='utf-8', tagName='record')
    
    print 'Loading'
    x = 0
    for doc in df:    
        x += 1
        
        doc = app.process_document(session, doc)
        rec = parser.process_document(session, doc)
        recordStore.create_record(session, rec)
        db.add_record(session, rec)

   
    x = 0
    print "Indexing records..."
    for rec in recordStore:    
        x += 1
        
        try:
            db.index_record(session, rec)
        except UnicodeDecodeError:
            print '[Some indexes not built - non unicode characters!]'






    db.commit_indexing(session)
    recordStore.commit_storing(session)
    db.commit_metadata(session)
    (mins, secs) = divmod(time.time() - start, 60)
    (hours, mins) = divmod(mins, 60)
    print 'Indexing complete (%dh %dm %ds)' % (hours, mins, secs)
