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
sys.path.insert(1,'/home/cheshire/cheshire3/code')

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')


dir = '/home/cheshire/cheshire3/dbs/istc/data/'

dict = { '~~' : '&#176;'
#        u'Sèlestat': u'S&#233;lestat',
#        u'Selestat': u'S&#233;lestat',
#        'Feldkirch,StB': 'Feldkirch, StB',
#        u'Kláater' : u'Kl&#225;&#353;ter',
#        u'Kl&#225;ater' : u'Kl&#225;&#353;ter',
#        u'Bucarest' : u'Bucharest'
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
    field9s = tree.xpath('//datafield[@tag="300"]/subfield|//datafield[@tag="500"]/subfield')
#    field9s = tree.xpath('//*[starts-with(@tag, "9")]/subfield[@code="a"]')
    for field in field9s:
        try:
            field.text = multiReplace(unicode(field.text), dict)
        except:
            pass
    for field in field9s:
        if field.text == '%F300_C%':
            parent = tree.xpath('//record')[0]
            parent.remove(tree.xpath('//datafield[@tag="300"]')[0])
            
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