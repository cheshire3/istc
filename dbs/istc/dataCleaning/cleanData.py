#!/home/cheshire/cheshire3/install/bin/python 
# -*- coding: utf-8 -*-
"""Clean up the character encoding problems when moving from C2 to C3 (June 2009)"""

import sys
import os
import re
import time

sys.path.insert(1, '/home/cheshire/cheshire3/code')

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


print 'cleaningData'

#listFiles = os.listdir("encodingtest/")
listFiles = os.listdir("/home/cheshire/cheshire3/dbs/istc/newData/")
parser = db.get_object(session, 'LxmlParser')
marcTxr = db.get_object(session, 'dataTransformer')
indentingTxr = db.get_object(session, 'indentingTxr')
istcnoregex = re.compile('<fld001>(\S*)</fld001>')
preparser = db.get_object(session, 'CharacterEntityPreParser')

forliRE = re.compile('Forl.*grave;')
LokkosRE = re.compile('LQkk.*s')
mondoviRE = re.compile('Mondov.*grave;')


errors = 0;
errorids = []
correct = 0;
for file in listFiles:
    #print file
    dataFile = open("/home/cheshire/cheshire3/dbs/istc/newData/" + file, 'r')
#    dataFile = open("encodingtest" + "/" + file, 'r')
    dataString = dataFile.read()
    dataString = forliRE.sub('Forl&#236;', dataString)
    dataString = mondoviRE.sub('Mondov&#236;', dataString)
    dataString = LokkosRE.sub('L&#337;kk&#246;s', dataString)
    dataString = dataString.replace('GdaDsk', 'Gda&#324;sk')
    dataString = dataString.replace('WrocBaw', 'Wroc&#322;aw')
    dataString = dataString.replace('WBocBawek', 'W&#322;oc&#322;awek')
    dataString = dataString.replace('PoznaD', 'Pozna&#324;')
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
        dataFile = open("/home/cheshire/cheshire3/dbs/istc/newData/" + file, 'r')
        dataString = dataFile.readlines() 
        newfile = []
        
        for l in dataString:
            l = forliRE.sub('Forl&#236;', l)
            l = mondoviRE.sub('Mondov&#236;', l)
            l = LokkosRE.sub('L&#337;kk&#246;s', l)
            l = l.replace('GdaDsk', 'Gda&#324;sk')
            l = l.replace('WrocBaw', 'Wroc&#322;aw')
            l = l.replace('WBocBawek', 'W&#322;oc&#322;awek')
            l = l.replace('PoznaD', 'Pozna&#324;')
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
            try:
                errorids.append(re.findall(istcnoregex, doc.get_raw(session))[0])
                print re.findall(istcnoregex, doc.get_raw(session))[0]
            except:
                print doc.get_raw(session)
            errors += 1   
        
#        dataWrite = open("encodingtest/all" + file, 'w')
    dataWrite = open("/home/cheshire/cheshire3/dbs/istc/data/" + file, 'w')
    dataWrite.write(output.get_raw(session))
    dataWrite.close
    dataFile.close
    

print 'Sucessful: %s' % correct
print 'Errors: %s' % errors
