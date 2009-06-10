#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

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



#put austria.xml into a tree for each element find the istc file which matches put that into a tree and add the stuff

input = open(cheshirePath + '/cheshire3/dbs/istc/austria.xml', 'r')

austriaTree = etree.fromstring(input.read())

for elem in austriaTree.iter('ISTC-Bestand'):
    
    istcNo = elem.xpath('./ISTC-Nr/text()')[0]
    data = elem.xpath('./Bestand/text()')[0]
    if data.find('(') != -1:
        maindata = data[:data.find('(')].strip()
        suppdata = data[data.find('('):].strip()
    else:
        maindata = data.strip()
        suppdata = None
    try:
        file = open(cheshirePath + '/cheshire3/dbs/istc/data/' + istcNo + '.xml', 'r')
    except:
        print istcNo
    else:
        targetTree = etree.fromstring(file.read())
        file.close()
        parent = targetTree.xpath('/record')[0]
        datafield = etree.Element('datafield', tag='993', ind1='0', ind2='0')
        
        subfieldA = etree.Element('subfield', code='a')   
        subfieldA.text = maindata
        datafield.append(subfieldA)
        
        if suppdata:
            subfieldB = etree.Element('subfield', code='b')   
            subfieldB.text = suppdata
            datafield.append(subfieldB)
        
        parent.append(datafield)
        doc = StringDocument(etree.tostring(targetTree))
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)     
        output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + istcNo + '.xml', 'w')
        output.write(doc2.get_raw(session))
        output.flush()
        output.close()
    
    
#    print 'istcno: %s - lib: %s' % (istcNo, data)