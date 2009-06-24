#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#gets all records with a single German library where that is not Munchen

import time, sys, os
sys.path.insert(1,'/home/cheshire/cheshire3/code')

import cheshire3

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument

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

for r in recordStore:
    if r.process_xpath(session, 'count(//datafield[@tag="997"])')[0] == 1:
        if  r.process_xpath(session, '//datafield[@tag="997"][1]/subfield[@code=\'a\']/text()')[0].strip() != u'München BSB':
            count += 1
            print txr.process_record(session, r).get_raw(session)
            #print r.process_xpath(session, '//controlfield[@tag="001"]')[0].text
            
#print 'total = %d' % count