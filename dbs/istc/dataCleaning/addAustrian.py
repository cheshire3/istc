#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to bulk load Austrian location data into field 993 when moving from C2 to C3 (June 2009)



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

input = open(cheshirePath + '/cheshire3/dbs/istc/dataCleaning/austria.xml', 'r')

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
        #create tree from ISTC record
        targetTree = etree.fromstring(file.read())
        file.close()
        parent = targetTree.xpath('/record')[0]
        
        # remove Austrian data from 958 Other Europe field
        otherEurope = targetTree.xpath('//datafield[@tag="958"]')
        for entry in otherEurope:
#            print etree.tostring(entry)
            if entry.xpath('./subfield[@code="a"]')[0].text.find('Salzburg') != -1:
                parent.remove(entry)
            elif entry.xpath('./subfield[@code="a"]')[0].text.find('Graz') != -1:
                parent.remove(entry)
            elif entry.xpath('./subfield[@code="a"]')[0].text.find('Innsbruck') != -1:
                parent.remove(entry)
            elif entry.xpath('./subfield[@code="a"]')[0].text.find('Wien') != -1:
                parent.remove(entry)
                
        # add new Austrian 993 field
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
    
    