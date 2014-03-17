#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-

#Used to change the German location data when moving from C2 to C3 (June 2009)

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


#Set this to true if you want to keep private data associated with the record false if you want to replace all the data
keepPrivate = True 

datadir = '/home/cheshire/cheshire3/dbs/istc/data'
outdir = '/home/cheshire/cheshire3/dbs/istc/dataTemp'
         
            
#add the new ones from the datafile
newData = '/home/cheshire/cheshire3/dbs/istc/dataCleaning/newGermanData.txt'

missing = []

print 'changing German data'
if "--location-per-line" in sys.argv:
    fh = codecs.open('/home/cheshire/cheshire3/dbs/istc/dataCleaning/Germanlocs2010.TXT', "r", "utf-8" )
    lines = fh.readlines()
    fh.close()
    for l in lines:
        l = l.strip()
        if not l:
            continue
        elif l.find('#RA#') == 0:
            number = l[l.find('i')-1:].replace('#', '')
            try:
                targetFile = open(os.path.join(datadir, number + '.xml'), 'r')
            except IOError:
                missing.append(number)
                number = None
                targetTree = None
            else:
                targetTree = etree.parse(targetFile)
    	        targetFile.close()
    	        parent = targetTree.getroot()
                #remove current 997 fields in record (including or not the private data depending on flag)
                germanlocs = targetTree.xpath('//datafield[@tag="997"]')
                if keepPrivate == True:
                    for entry in germanlocs:
                        if not entry.xpath('./subfield[@code="x"]'):
                            parent.remove(entry)
                else:
                    for entry in germanlocs:
                        parent.remove(entry)
            # move on to data line(s)
            continue
        try:
            parent = targetTree.getroot()
        except (NameError, AttributeError):
            continue
        #create new 997 node
        datafield = etree.Element('datafield', tag='997', ind1='0', ind2='0')
        data = l[10:].strip(' $#')
        fieldsList = data.split('$')
	    # for each MARC sub-field
        for field in fieldsList:
            sfcode, field = field[0], field[1:]
            subfield = etree.Element('subfield', code=sfcode)
            subfield.text = field.replace('*', '')
            datafield.append(subfield)
        parent.append(datafield)
        doc = StringDocument(etree.tostring(targetTree))
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)     
        output = open(os.path.join(outdir, number + '.xml'), 'w')
        output.write(doc2.get_raw(session))
        output.flush()
        output.close()
        
else:
    file = codecs.open( newData, "r", "utf-8" )
    lines = file.readlines()
    file.close()

    for i, l in enumerate(lines):
        if (len(l.strip()) > 0 and l.strip().find('#RA#') == 0):
            number = l.strip()[l.find('i')-1:].replace('#', '')
            data = lines[i+1].strip()[10:].strip().replace('#', '')
            dataList = data.split(';')
            try:
                targetFile = open(os.path.join(datadir, number + '.xml'), 'r')
            except:
                missing.append(number)
            else:
                targetTree = etree.fromstring(targetFile.read())
                targetFile.close()
                parent = targetTree.xpath('/record')[0]        
                #remove current 997 fields in record (including or not the private data depending on flag)
                germanlocs = targetTree.xpath('//datafield[@tag="997"]')
                if keepPrivate == True:
                    for entry in germanlocs:
                        if not entry.xpath('./subfield[@code="x"]'):
                            parent.remove(entry)
                else:
                    for entry in germanlocs:
                        parent.remove(entry)
                for d in dataList:
                    d = d.strip()
                    #create new 997 node
                    datafield = etree.Element('datafield', tag='997', ind1='0', ind2='0')
                    if d.find(' (') == -1:
                        subfieldA = etree.Element('subfield', code='a')   
                        subfieldA.text = d.replace('*', '')
                        datafield.append(subfieldA) 
                    else:
                        subfieldA = etree.Element('subfield', code='a')   
                        subfieldA.text = d[:d.find(' (')].replace('*', '')
                        datafield.append(subfieldA)
                        
                        subfieldB = etree.Element('subfield', code='b')   
                        subfieldB.text = d[d.find(' (')+1:].replace('*', '')
                        datafield.append(subfieldB)
                    if d.find('*') != -1:
                        subfieldX = etree.Element('subfield', code='x')
                        subfieldX.text = 'Private'
                        datafield.append(subfieldX)
                        
                    parent.append(datafield)
                    doc = StringDocument(etree.tostring(targetTree))
                    rec = parser.process_document(session, doc)
                    doc2 = indentingTxr.process_record(session, rec)     
                    output = open(os.path.join(outdir, number + '.xml'), 'w')
                    output.write(doc2.get_raw(session))
                    output.flush()
                    output.close()
    	
#print 'MISSING FROM GERMAN'
#print '\n'.join(missing)
missingFile = open('missingITSCs.txt', 'w')
for l in missing:
	missingFile.write(l + '\n')
	missingFile.flush()
missingFile.close()

