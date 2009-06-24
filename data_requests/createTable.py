#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#creates table of all records containing bsb-ink in 510 field


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

output = []

for rec in recStore:
    #print rec
    if len(rec.process_xpath(session, '//datafield[@tag="510"]')):
        #print 'has tag'
        for e in rec.process_xpath(session, 'datafield[@tag="510"]/subfield'):
            if e.text.lower().find('bsb-ink') != -1 :
                output.append('<tr><td>%s</td><td>%s</td></tr>' % (rec.process_xpath(session, '//controlfield[@tag="001"]/text()')[0], e.text))
                #print output
                
table = '<table>%s</table>' % ''.join(output)                
    
tableFile = codecs.open('ISTCtable.xml', 'w', 'utf-8')

tableFile.write(table)

tableFile.close()
print table
