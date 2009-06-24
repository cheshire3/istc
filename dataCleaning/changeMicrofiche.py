#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to change wording of Microfiche data when moving from C2 to C3 (June 2009)

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


#remove 530 tags with the word microfiche in them
dir = '/home/cheshire/cheshire3/dbs/istc/data/'

for f in os.listdir(dir):
    file = open(dir + f, 'r')
    targetTree = etree.fromstring(file.read())
    file.close()
    
    parent = targetTree.xpath('/record')[0]
    
    
    microfiche = targetTree.xpath('//datafield[@tag="530"]')
    for entry in microfiche:
        if entry.xpath('./subfield[@code="a"]')[0].text == None:
            pass
        elif entry.xpath('./subfield[@code="a"]')[0].text.lower().find('microfiche') != -1:
            parent.remove(entry)
        
    doc = StringDocument(etree.tostring(targetTree))
    rec = parser.process_document(session, doc)
    doc2 = indentingTxr.process_record(session, rec)     
    output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + f, 'w')
    output.write(doc2.get_raw(session))
    output.flush()
    output.close()
            
            
#add the new ones from the datafile
newData = '/home/cheshire/cheshire3/dbs/istc/dataCleaning/newMicroficheData.txt'

file = open(newData, 'r')
lines = file.readlines()
file.close()
missing = []

for l in lines:
    if len(l.strip()) > 0:
        number = l[:l.find('.')]
        text = l[l.find('$a')+2:].strip()
        try:
            targetFile = open(dir + number + '.xml', 'r')
        except:
            missing.append(number)
        else:
            targetTree = etree.fromstring(targetFile.read())
            targetFile.close()
            
            parent = targetTree.xpath('/record')[0]
            
            #create new 530 node
            datafield = etree.Element('datafield', tag='530', ind1='0', ind2='0')
            
            subfieldA = etree.Element('subfield', code='a')   
            subfieldA.text = text
            datafield.append(subfieldA)
            
            #find last 510 node
            last510 = targetTree.xpath('//datafield[@tag="510"]')[-1]
            parent.insert(targetTree.index(last510) + 1, datafield)
            doc = StringDocument(etree.tostring(targetTree))
            rec = parser.process_document(session, doc)
            doc2 = indentingTxr.process_record(session, rec)     
            output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + number + '.xml', 'w')
            output.write(doc2.get_raw(session))
            output.flush()
            output.close()
              
            
print '\n'.join(missing)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        