#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to recover all the 530 fields lost in the first release of the editor - oooops



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

backupData = '/home/cheshire/cheshire3/dbs/istc/backupData/'
liveData = '/home/cheshire/cheshire3/dbs/istc/data/'

for record in os.listdir(backupData):
#    file = codecs.open( backupData + record, "r", "utf-8" )
    file = open(backupData + record, 'r')
    backupTree = etree.fromstring(file.read())
    file.close()
    
    #see if backup file has 530 field and if not move onto the next record
    field530 = backupTree.xpath('//datafield[@tag="530"]')
    
    if len(field530) > 0:
        
        #find the live version of the record and see if that has a 530 field already if not add it if so ignore it      
 #       file = codecs.open( liveData + record, "r", "utf-8" )
        file = open(liveData + record, 'r')
        liveTree = etree.fromstring(file.read())
        file.close()
        
        if len(liveTree.xpath('//datafield[@tag="530"]')) == 0:
            print record
            #get the data from the backup record
            
            for i, f in enumerate(field530):
                if len(f.xpath('./subfield[@code="a"]')) > 0:
                    texta = f.xpath('./subfield[@code="a"]/text()')[0]
                else:
                    texta = None
                if len(f.xpath('./subfield[@code="u"]/text()')) > 0:
                    textu = f.xpath('./subfield[@code="u"]/text()')[0]
                else:
                    textu = None
                #create new node
                datafield = etree.Element('datafield', tag='530', ind1='0', ind2='0')
                if texta != None:
                    subfieldA = etree.Element('subfield', code='a')   
                    subfieldA.text = texta
                    datafield.append(subfieldA)
                if textu != None:
                    subfieldU = etree.Element('subfield', code='u')   
                    subfieldU.text = textu
                    datafield.append(subfieldU)
                
                parent = liveTree.xpath('/record')[0]
                if i == 0:
                    #add it  after 510 field
                    last510 = liveTree.xpath('//datafield[@tag="510"]')[-1]
                    parent.insert(liveTree.index(last510) + 1, datafield)
                else:
                    #add it after the last 530 field
                    last530 = liveTree.xpath('//datafield[@tag="530"]')[-1]
                    parent.insert(liveTree.index(last530) + 1, datafield)
                
            doc = StringDocument(etree.tostring(liveTree))
            rec = parser.process_document(session, doc)
            doc2 = indentingTxr.process_record(session, rec)     
            output = open(liveData + record, 'w')
            output.write(doc2.get_raw(session))
            output.flush()
            output.close()
                
                

