#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

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
defpath = db.get_path(session, "defaultPath")
recordStore = db.get_object(session, 'recordStore')
qf = db.get_object(session, 'baseQueryFactory')
parser = db.get_object(session, 'LxmlParser')
txr = db.get_object(session, 'toMarcTxr')

count = 0

output = []

f = codecs.open('/home/cheshire/cheshire3/dbs/istc/data_requests/CengageExchange.txt', 'w', 'UTF-8')

for r in recordStore:
    if r.process_xpath(session, 'count(//datafield[@tag="530"])'):
        list = r.process_xpath(session, '//datafield[@tag="530"]/subfield[@code=\'a\']/text()')
        for l in list:
            if l.find('Microfiche') == 0 and count < 20:
                           
                count += 1                
                
                reqdtags = ['001', '003', '008', '100', '130', '245', '260', '300', '510', '530']
                
                oldtree = etree.fromstring(r.get_xml(session))

                newtree = etree.Element('record')
                
                for element in oldtree.iterchildren():

                    if element.get('tag') in reqdtags or element.tag == 'leader':
                        newtree.append(element)
         
                doc = StringDocument(etree.tostring(newtree))
                rec = parser.process_document(session, doc)
                
                output.append(txr.process_record(session, rec).get_raw(session))
             
f.write(''.join(output)) 
f.flush()
f.close()               

    
            
