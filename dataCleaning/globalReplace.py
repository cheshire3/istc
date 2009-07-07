#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-


#Used to some global data corrections when moving from C2 to C3 (June 2009)



import time, sys, os
from lxml import etree
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
from cheshire3.web.www_utils import *
cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')


dir = '/home/cheshire/cheshire3/dbs/istc/data/'

dict = {'S&#232;lestat': 'S&#233;lestat',
        'Feldkirch,StB': 'Feldkirch, StB',
        'Kl&#225;ater' : 'Tepl&#225; Kl&#225;&#353;ter'
#        'Wellcome Institute': 'Wellcome Library',
#        'Oslo UB' :'Oslo NL',
#        'Oslo NB' :'Oslo NL',
#        'Kiev Akad' : 'Kiev NL',
#        'Helsinki UL' : 'Helsinki NL',
#        'V&#228;ster&#229;s LB'  : 'V&#228;ster&#229;s StB',
#        'Olomouc UKn' : 'Olomouc VKn'      
    }


for f in os.listdir(dir):
    file = open(dir + f, 'r')
    tree = etree.fromstring(file.read())
    file.close()
    field9s = tree.xpath('//*[starts-with(@tag, "9")]/subfield[@code="a"]')
    for field in field9s:
        try:
            field.text = multiReplace(field.text, dict)
        except:
            pass
    dataString = etree.tostring(tree)
    dataString = dataString.replace('&amp;#', '&#')
    dataString = dataString.replace('&amp;amp;', '&amp;')
    doc = StringDocument(dataString)
    rec = parser.process_document(session, doc)
    doc2 = indentingTxr.process_record(session, rec)     
    output = open(dir + f, 'w')
    output.write(doc2.get_raw(session))
    output.flush()
    output.close()