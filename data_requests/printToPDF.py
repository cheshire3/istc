#prints all of the ISTC or a specific letter set of the ISTC to a pdf - this can be done in the admin interface but it takes such a long time that it may
#not be reliable so this is a backup in case the interface can't handle it.

import time, sys, os
sys.path.insert(1,'/home/cheshire/cheshire3/code')

import cheshire3

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
from lxml import etree
import codecs
import getpass
from crypt import crypt

cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
recordStore = db.get_object(session, 'recordStore')
qf = db.get_object(session, 'baseQueryFactory')


all = True
letters = 'ia'

output = []
df = db.get_object(session, 'reportLabDocumentFactory')


if all == True:
    for rec in recordStore:            
        df.load(session, rec)
    doc = df.get_document(session)
    
else :
    q = qf.get_query(session, 'c3.idx-ISTCnumber any %s*' % letters)
    rs = db.search(session, q)
    if len(rs):
        for r in rs:
            df.load(session, r.fetch_record(session))
        doc = df.get_document(session)
    else:
        print 'no records found'
    
    
file = open('istc.pdf', 'w')
file.write(doc.get_raw(session))
file.flush()
file.close()
    

#
#def print_alphaSelection(letters):
#    output = []
#    df = db.get_object(session, 'reportLabDocumentFactory')
#    q = qf.get_query(session, 'c3.idx-ISTCnumber any %s*' % letters)
#    rs = db.search(session, q)
#    if len(rs):
#        for r in rs:
#            df.load(session, r.fetch_record(session))
#        doc = df.get_document(session)
#        return doc.get_raw(session)

    

#def print_all():
#    output = []
#    df = db.get_object(session, 'reportLabDocumentFactory')
#    for rec in recordStore:            
#        df.load(session, rec)
#    doc = df.get_document(session)
#    return doc.get_raw(session)