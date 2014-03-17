#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to change the Structure on 510 and the indicator values data when moving from C2 to C3 (August 2009)

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

#remove all 997 tags 
dir = '/home/cheshire/cheshire3/dbs/istc/data/'

for f in os.listdir(dir):
    file = open(dir + f, 'r')
    tree = etree.fromstring(file.read())
    file.close()
    
    for node in tree.iter():
        if node.tag == 'datafield':
            if node.get('tag') == '100':
                node.set('ind2', ' ')
            if node.get('tag') == '130':
                node.set('ind1', '0')
                node.set('ind2', ' ')
            if node.get('tag') == '245':
                node.set('ind2', '0')
            if node.get('tag') == '260':
                node.set('ind1', ' ')
                node.set('ind2', ' ')
            if node.get('tag') == '300':
                node.set('ind1', ' ')
                node.set('ind2', ' ')   
            if node.get('tag') == '500':
                node.set('ind1', ' ')
                node.set('ind2', ' ')  
            if node.get('tag') == '510':
                node.set('ind1', '4')
                node.set('ind2', ' ')
            if node.get('tag') == '530':
                node.set('ind1', ' ')
                node.set('ind2', ' ')               
            if node.get('tag') == '852':
                node.set('ind1', ' ')
                node.set('ind2', ' ')    
            if node.get('tag').find('9') == 0:
                node.set('ind1', ' ')
                node.set('ind2', ' ') 
                
    leaderNode = tree.xpath('//leader')[0]         
    leader = leaderNode.text

    newleaderlist=([''.join(leader[:5]), 'nam a', ''.join(leader[10:17]), '7', ''.join(leader[18:])])
    newleader = ''.join(newleaderlist)
    leaderNode.text = newleader



    field510 = tree.xpath('//datafield[@tag="510"]')   
    for node in field510:
        data = node.xpath('./subfield[@code="a"]')[0].text

        node.remove(node.xpath('./subfield[@code="a"]')[0])

        ref = data.replace('*', '\*').replace('?', '\?').replace('"', ' ').replace('\'', ' ')
        session.database = db3.id
        q = qf.get_query(session, 'c3.idx-key-refs exact "%s"' % (ref))
        rs = db3.search(session, q)
        if len(rs):
            finalRef = ref
        else :
            while ref.rfind(' ') != -1 and not len(rs):
                ref = ref[:ref.rfind(' ')].strip()
                q.term.value = ref
                rs = db3.search(session, q)
            if len(rs):
                finalRef = ref
            else:
                finalRef = data


        codeA = etree.Element('subfield', code='a')
        codeA.text = finalRef.strip()
        node.append(codeA)
        locationInRef = data[data.find(finalRef)+len(finalRef):].strip()
        if locationInRef != '':
            codeC = etree.Element('subfield', code='c')
            codeC.text = locationInRef
            node.append(codeC)
        
        
    doc = StringDocument(etree.tostring(tree))
    rec = parser.process_document(session, doc)
    doc2 = indentingTxr.process_record(session, rec)     
    output = open(dir + f, 'w')
    output.write(doc2.get_raw(session))
    output.flush()
    output.close()
        
    
    
    
    
               
                
                
                
                                               