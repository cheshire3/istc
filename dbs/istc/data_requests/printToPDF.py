#prints all of the ISTC or a specific letter set of the ISTC to a pdf - this can be done in the admin interface but it takes such a long time that it may
#not be reliable so this is a backup in case the interface can't handle it.

import time, sys, os
sys.path.insert(1,'/home/cheshire/cheshire3/code')

import cheshire3

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument
from lxml import etree
import codecs
import getpass
from crypt import crypt

cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
dbusa = serv.get_object(session, 'db_usa')
recordStore = db.get_object(session, 'recordStore')
qf = db.get_object(session, 'baseQueryFactory')
txr = db.get_object(session, 'printAllTxr')
xmlp = db.get_object(session, 'LxmlParser')
externalDataTxr = db.get_object(session, 'externalDataTxr')

all = True
letters = 'ia'



def get_usaRefs(session, rec):
    session.database = dbusa.id
    usaRefs = []
    otherDict = {}
    qstring = []
    for node in rec.process_xpath(session, '//datafield[@tag="952"]'):
        ref = node.xpath('subfield[@code="a"]/text()')[0]
        other = node.xpath('subfield[@code="b"]/text()')
        if len(other):
            other = ' %s' % ' '.join(other)
        else:
            other = ''
        otherDict[ref] = other
        qstring.append('c3.idx-key-usa exact "%s"' % ref)
    if len(qstring) > 0:
        q = qf.get_query(session, ' or '.join(qstring))
        rs = dbusa.search(session, q)
        idx = dbusa.get_object(session, 'idx-location_usa')
        rs.order(session, idx)
        for r in rs:
            rec = r.fetch_record(session)
            usaRefs.append('%s%s' % (rec.process_xpath(session, '//full/text()')[0].strip(), otherDict[rec.process_xpath(session, '//code/text()')[0].strip()]))
        return externalDataTxr.process_record(session, xmlp.process_document(session, StringDocument('<string>%s</string>' % '; '.join(usaRefs).encode('utf-8').replace('&', '&amp;')))).get_raw(session).replace('&', '&amp;')
    else:
        return ''




output = []
df = db.get_object(session, 'reportLabDocumentFactory')


if all == True:
    for record in recordStore:    
        print record.id  
        doc = txr.process_record(session, record)
        string = doc.get_raw(session)               
        string = string.replace('%usalocs%', get_usaRefs(session, record))
        session.database = 'db_istc'
        doc = StringDocument(string)
        rec = xmlp.process_document(session, doc)
        df.load(session, rec)      
    doc = df.get_document(session)
    
else :
    q = qf.get_query(session, 'c3.idx-ISTCnumber any %s*' % letters)
    rs = db.search(session, q)
    if len(rs):
        for r in rs:
            record = r.fetch_record(session)
            print record.id
            doc = txr.process_record(session, record)
            string = doc.get_raw(session)               
            string = string.replace('%usalocs%', get_usaRefs(session, record))
            session.database = 'db_istc'
            doc = StringDocument(string)
            rec = xmlp.process_document(session, doc)
            df.load(session, rec)
        doc = df.get_document(session)
    else:
        print 'no records found'
    
    
file = open('istc.pdf', 'w')
file.write(doc.get_raw(session))
file.flush()
file.close()
    
