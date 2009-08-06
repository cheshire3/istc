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
    
    
    facsimile = targetTree.xpath('//datafield[@tag="530"]')
    for entry in facsimile:
        if entry.xpath('./subfield[@code="a"]')[0].text == None:
            pass
        elif entry.xpath('./subfield[@code="a"]')[0].text.lower().find('electronic') != -1 and entry.xpath('./subfield[@code="a"]')[0].text.lower().find('bayerische') != -1:
            parent.remove(entry)
        
    doc = StringDocument(etree.tostring(targetTree))
    rec = parser.process_document(session, doc)
    doc2 = indentingTxr.process_record(session, rec)     
    output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + f, 'w')
    output.write(doc2.get_raw(session))
    output.flush()
    output.close()
    
#add the new ones from the datafile
newData = '/home/cheshire/cheshire3/dbs/istc/dataCleaning/istcdig.xml'    

file = open(newData, 'r')
newtree = etree.fromstring(file.read())
file.close()

bsbDict = {}

incunab = newtree.xpath('//incunabulum')


for entry in incunab:
    BSBno = entry.xpath('./bsb-ink')[0].text
    if entry.xpath('./dig-art')[0].text == 'ZEND' or entry.xpath('./dig-art')[0].text == 'Einblattdruck':
        bsbDict[BSBno] = 'http://mdzx.bib-bvb.de/bsbink/Ausgabe_%s.html' % BSBno


for f in os.listdir(dir):
    file = open(dir + f, 'r')
    targetTree = etree.fromstring(file.read())
    file.close()
    
    parent = targetTree.xpath('/record')[0]
    
    refs = targetTree.xpath('//datafield[@tag="510"]/subfield[@code="a"]')
    url = None
    for ref in refs:
        if ref.text.find('BSB-Ink') != -1:

            BSBno = ref.text[ref.text.find(' ')+1:] 
            if BSBno.find(' ') != -1:
                BSBno = BSBno[:BSBno.find(' ')]       
            try:
                url = bsbDict[BSBno]
            except:
                try:
                    url = bsbDict['(%s)' % BSBno]
                    BSBno = '(%s)' % BSBno
                except:
                    pass

    if url != None:
       #create new 530 node
        datafield = etree.Element('datafield', tag='530', ind1='0', ind2='0')
        
        subfieldA = etree.Element('subfield', code='a')   
        subfieldA.text = 'Electronic facsimile : Bayerische Staatsbibliothek, M&#252;nchen'
        datafield.append(subfieldA)
        
        subfieldU = etree.Element('subfield', code='u')
        subfieldU.text = url
        datafield.append(subfieldU)
    
    
        last510 = targetTree.xpath('//datafield[@tag="510"]')[-1]
        parent.insert(targetTree.index(last510) + 1, datafield)
        dataString = etree.tostring(targetTree)
        dataString = dataString.replace('&amp;#', '&#')
        dataString = dataString.replace('&amp;amp;', '&amp;')
        doc = StringDocument(dataString)
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)     
        output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + f, 'w')
        output.write(doc2.get_raw(session))
        output.flush()
        output.close()

            