#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

import time, sys, os
#osp = sys.path
#sys.path = ["/home/cheshire/cheshire3/cheshire3/code"]
#sys.path.extend(osp)
from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
from PyZ3950 import CQLParser
import getpass
from crypt import crypt
import codecs

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
recStore = db.get_object(session, 'recordStore')
sax = db.get_object(session, 'SaxParser')
authStore = db.get_object(session, 'istcAuthStore')

df = db.get_object(session, 'defaultDocumentFactory')
parser = db.get_object(session, 'LxmlParser')
app = db.get_object(session, 'AmpPreParser')
filter = db.get_object(session, 'filterTxr')
txr = db.get_object(session, 'toMarcTxr')
txtTxr = db.get_object(session, 'toTextTxr')
indentTxr = db.get_object(session, 'indentingTxr')

#queryList = ['c3.idx-951 all "Cambridge" and c3.idx-951 all "UL"']
queryList = ['c3.idx-951 all "JRL"']
fileE = codecs.open('Manchester-exchange.txt', 'w', 'utf-8')
fileA = codecs.open('Manchester-aleph.txt', 'w', 'utf-8')
fileX = codecs.open('Manchester-marcxml.xml', 'w', 'utf-8')
for query in queryList :
    q = CQLParser.parse(query)
    rs = db.search(session, q)
    i = 0
    for r in rs:
        
        rec = r.fetch_record(session)
        filtered = filter.process_record(session, rec)       
        rec2 = parser.process_document(session, filtered)
        if len(rec2.process_xpath(session, '//datafield[@tag="951"]')):
       # print txtTxr.process_record(session, rec2).get_raw(session)
            i += 1
            fileE.write(txr.process_record(session, rec2).get_raw(session))
            fileE.write('\n')
            fileA.write('\n\nMARC\n')
            fileA.write(txtTxr.process_record(session, rec2).get_raw(session))
            fileX.write(indentTxr.process_record(session, rec2).get_raw(session))
            print i
fileE.close()
fileA.close()
fileX.close()