#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to control field 003 when moving from C2 to C3 (June 2009)



import time, sys, os
from lxml import etree
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')


dir = '/home/cheshire/cheshire3/dbs/istc/data/'

for f in os.listdir(dir):
    file = open(dir + f, 'r')
    targetTree = etree.fromstring(file.read())
    file.close()
    
    parent = targetTree.xpath('/record')[0] 

    controlfield = etree.Element('controlfield', tag='003')
    controlfield.text = 'Uk-IS'
    
    controlfield001 = targetTree.xpath('//controlfield[@tag="001"]')[-1]
    parent.insert(targetTree.index(controlfield001) + 1, controlfield)
    
    dataString = etree.tostring(targetTree)
    doc = StringDocument(dataString)
    rec = parser.process_document(session, doc)
    doc2 = indentingTxr.process_record(session, rec)     
    output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + f, 'w')
    output.write(doc2.get_raw(session))
    output.flush()
    output.close()