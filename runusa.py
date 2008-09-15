#!/home/cheshire/install/bin/python -i

import time, sys, os

sys.path.insert(1,'/home/cheshire/cheshire3/cheshire3/code')

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
import cheshire3.exceptions
import lex, yacc
import random



# Build environment...
session = Session()
serv = SimpleServer(session, "/home/cheshire/cheshire3/cheshire3/configs/serverConfig.xml")

session.database = 'db_usa'
db = serv.get_object(session, 'db_usa')
defpath = db.get_path(session, "defaultPath")
recordStore = db.get_object(session, 'usaRecordStore')
sax = db.get_object(session, 'SaxParser')


df = db.get_object(session, 'defaultDocumentFactory')
parser = db.get_object(session, 'LxmlParser')
app = db.get_object(session, 'AmpPreParser')
    
       


if '-load' in sys.argv:
    start = time.time()
    #flow = db.get_object(session, 'buildIndexWorkflow')


    
    db.begin_indexing(session)
    recordStore.begin_storing(session)
    df.load(session, defpath + "/usaData/", codec='iso-8859-1', tagName='record')
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
