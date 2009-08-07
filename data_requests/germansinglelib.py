#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-
#SECOND, you produced a list of ISTC numbers a short time ago for ISTC records where there was only one 997 field, i.e. only one holding library in Germany.
#
#Bettina in Munich would be ecstatic if you were able to do something similar again based on our current data, but this time ouputting not just the ISTC number but a group of fields:
#
#ISTC  number
#100  Author
#130  Heading
#260  Imprint
#300  format
#510  Bibrefs
#997  German location
#
#and would be even more ecstatic if it were possible to sort the output by the German location (and then ISTC number within each location).
#gets all records with a single German library where that is not Munchen

import time, sys, os
sys.path.insert(1,'/home/cheshire/cheshire3/code')

import cheshire3

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
from lxml import etree

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
txr = db.get_object(session, 'toTextTxr')

count = 0

dict = {}

for r in recordStore:
    if r.process_xpath(session, 'count(//datafield[@tag="997"])')[0] == 1:
        if  r.process_xpath(session, '//datafield[@tag="997"][1]/subfield[@code=\'a\']/text()')[0].strip() != u'München BSB':
            count += 1
            
            reqdtags = ['001', '100', '130', '260', '300', '510', '997']
            
            oldtree = etree.fromstring(r.get_xml(session))
            #write filter!
            newtree = etree.Element('record')
            
            for element in oldtree.iterchildren():
                if element.get('tag') in reqdtags:
                    newtree.append(element)
     
            doc = StringDocument(etree.tostring(newtree))
            rec = parser.process_document(session, doc)
            
            key = '%s_%s' % (newtree.xpath('//datafield[@tag="997"]/subfield[@code="a"]/text()')[0], newtree.xpath('//controlfield[@tag="001"]/text()')[0])
            dict[key] = txr.process_record(session, rec).get_raw(session)
            
keys = dict.keys()
keys.sort()

f = open('/home/cheshire/cheshire3/dbs/istc/data_requests/GermanSingleLibData.txt', 'w')

for k in keys:
    f.write(dict[k])
    f.write('\n\n')
    
f.flush()
f.close()
    
            
            #create a dictionary with the key being German loc and istcno. Sort keys and then extract full records.
            
            
            
            #print txr.process_record(session, r).get_raw(session)
            #print r.process_xpath(session, '//controlfield[@tag="001"]')[0].text
            
#print 'total = %d' % count