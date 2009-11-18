#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to create a concordance of BSB-Ink numbers against ISTC numbers  

import time, sys, os, codecs
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
serv = SimpleServer(session, '/home/cheshire/cheshire3/configs/serverConfig.xml')
db3 = serv.get_object(session, 'db_refs')
qf = db3.get_object(session, 'DefaultQueryFactory')   


dir = '/home/cheshire/cheshire3/dbs/istc/data/'

output = []

for f in os.listdir(dir):
    file = open(dir + f, 'r')
    tree = etree.fromstring(file.read())
    file.close()


    field510 = tree.xpath('//datafield[@tag="510"]')   
    for node in field510:
        data = node.xpath('./subfield[@code="a"]')[0].text
        if data.find('BSB-Ink') == 0:
            output.append(data)
            output.append(' ')
            output.append(node.xpath('./subfield[@code="c"]')[0].text)
            output.append('\t')
            output.append(tree.xpath('//controlfield[@tag="001"]')[0].text)
            output.append('\n')
            
   
outfile = open('/home/cheshire/cheshire3/dbs/istc/data_requests/bsbConcordance.txt', 'w')
outfile.write(''.join(output))
outfile.flush()
outfile.close()
        
    
    
    
    
               
                
                
                



