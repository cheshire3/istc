#!/home/cheshire/cheshire3/install/bin/python 
# -*- coding: utf-8 -*-

import time, sys, os, re

sys.path.insert(1,'/home/cheshire/cheshire3/code')

from cheshire3.web import www_utils
from cheshire3.web.www_utils import *
from cheshire3.document import StringDocument
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer

cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')



#listFiles = os.listdir("encodingtest/")
listFiles = os.listdir("oldformdata/")
parser = db.get_object(session, 'LxmlParser')
marcTxr = db.get_object(session, 'dataTransformer')
indentingTxr = db.get_object(session, 'indentingTxr')
istcnoregex = re.compile('<fld001>(\S*)</fld001>')
preparser = db.get_object(session, 'CharacterEntityPreParser')

errors = 0;
errorids = []
correct = 0;
for file in listFiles:
    #print file
    dataFile = open("oldformdata" + "/" + file, 'r')
#    dataFile = open("encodingtest" + "/" + file, 'r')
    dataString = dataFile.read()
    dataString = dataString.replace('&', '&amp;')
    dataString = dataString.replace('', '&#263;').replace('', '&#281;').replace('', '')
    dataString = dataString.replace('&amp;#', '&#')
    dataString = dataString.replace('&amp;amp;', '&amp;')

    #extrabits
    doc = StringDocument(dataString)   
    try:
        rec = parser.process_document(session, doc)
        output = marcTxr.process_record(session, rec)
        rec = parser.process_document(session, output)
        output = indentingTxr.process_record(session, rec)
        correct += 1
    except:
        errorids.append(re.findall(istcnoregex, doc.get_raw(session))[0])
#        print re.findall(istcnoregex, doc.get_raw(session))[0]
#            raise
    
    else:
        
#        dataWrite = open("encodingtest/all" + file, 'w')
        dataWrite = open("data/" + file, 'w')
        dataWrite.write(output.get_raw(session))
        dataWrite.close
        dataFile.close
    
for id in errorids:
    
    dataFile = open("oldformdata/" + id + '.xml', 'r')
    dataString = dataFile.readlines() 
    newfile = []
    for l in dataString:
        l = l.replace('&', '&amp;')
        l = l.replace('', '&#263;').replace('', '&#281;').replace('', '')
        l = l.replace('&amp;#', '&#')
        l = l.replace('&amp;amp;', '&amp;')
        try:
            l = l.decode('utf-8')
        except:
            l = l.decode('iso-8859-1')
        newfile.append(l)
        
    doc = StringDocument(' '.join(newfile))
    try:
        rec = parser.process_document(session, doc)
        output = marcTxr.process_record(session, rec)
        rec = parser.process_document(session, output)
        output = indentingTxr.process_record(session, rec)
        correct += 1
    except:
        errorids.append(re.findall(istcnoregex, doc.get_raw(session))[0])
        print re.findall(istcnoregex, doc.get_raw(session))[0]
        errors += 1
        
    else:
 #       dataWrite = open("encodingtest/all" + file, 'w')
        dataWrite = open("data/" + file, 'w')
        dataWrite.write(output.get_raw(session))
        dataWrite.close
        dataFile.close

print 'Sucessful: %s' % correct
print 'Errors: %s' % errors