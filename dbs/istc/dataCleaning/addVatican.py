#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-
"""Script to bulk load Vatican location data from provided MARCXML 
file into field 954."""

import sys
import os
import codecs

from lxml import etree

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.record import LxmlRecord
cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')

NSMAP = {'marc': "http://www.loc.gov/MARC21/slim"}

# Read and parse Vatican data MARC XML file into etree


marcfp = os.path.join(cheshirePath, 
					'cheshire3', 
					'dbs', 
					'istc', 
					'dataCleaning', 
					'marcxml_VISTC.xml')
print "Reading Vatican data from", marcfp

with open(marcfp, 'r') as marcfh:
    marcTree = etree.parse(marcfh)

missing035 = open('Vatican_missing_035.xml', 'w')
missing035.write('''\
<?xml version="1.0" encoding="UTF-8" ?>
<marc:collection xmlns:marc="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">''')
manual035 = codecs.open('Vatican_manual_035.txt', 'w', 'utf-8')
notInISTC = codecs.open('Vatican_035_not_in_ISTC.txt', 'w', 'utf-8')
missingShelf = codecs.open('Vatican_missing_shelfmark.txt', 'w', 'utf-8')

for marcrec in marcTree.iter(tag='{http://www.loc.gov/MARC21/slim}record'):
    try:
        istcNo = marcrec.xpath("./marc:datafield[@tag='035']/marc:subfield[@code='a']/text()", namespaces=NSMAP)[0]
    except IndexError:
        missing035.write(etree.tostring(marcrec, encoding='utf-8'))
        continue
        
    if not istcNo.startswith('(Uk-IS)'):
        manual035.write(istcNo)
        manual035.write('\n')
        continue
        
    istcNo = istcNo[7:]
    istcfp = os.path.join(cheshirePath,
						   'cheshire3', 
						   'dbs', 
						   'istc', 
						   'data',
						   u'{0}.xml'.format(istcNo))
    try:
        istcfh = open(istcfp, 'r')
    except:
        notInISTC.write(istcNo)
        notInISTC.write('\n')
        continue
    else:
        print istcNo
        #create tree from ISTC record
        targetTree = etree.parse(istcfh)
        istcfh.close()
        recEl = targetTree.xpath('/record')[0]
        # targetEl will be the 954 Vatican field
        targetEl = None
        for locEl in recEl.xpath("./datafield[@tag='954']"):
            if etree.tostring(locEl, method="text", encoding="utf-8").find('Vatican') > -1:
                try:
                    holdingEl = locEl.xpath("./subfield[@code='b']")[0]
                except IndexError:
                    pass
                else:
                    locEl.remove(holdingEl)
                targetEl = locEl
        # if 954 Vatican field not found in record
        if targetEl is None:
            # add new 954 Vatican field
            targetEl = etree.Element('datafield', tag='954', ind1='0', ind2='0')
            subfieldA = etree.Element('subfield', code='a')   
            subfieldA.text = "Vaticano BAV"
            targetEl.append(subfieldA)
            # find correct place to insert into record
            # count down from 954 field
            for x in range(954, 1, -1):
                try:
                    insertAfter = recEl.xpath("./datafield[@tag='{0}']".format(x))[-1]
                except:
                    # field doesn't exist, continue
                    continue
                else:
                    insertPosition = recEl.index(insertAfter) + 1
                    break
            recEl.insert(insertPosition, targetEl)
        
        # find new locations data
        locations = marcrec.xpath("./marc:datafield[@tag='852']/marc:subfield[@code='h']/text()", namespaces=NSMAP)

        if locations:
            subfieldB = etree.Element('subfield', code='b')
            if len(locations) == 1:
            	subfieldB.text = locations[0]
            else:
                subfieldB.text = u"({0}: {1})".format(len(locations), u', '.join(locations))
            targetEl.append(subfieldB)
        else:
            missingShelf.write(istcNo)
            missingShelf.flush()
            continue
        
        rec = LxmlRecord(recEl)
        doc = indentingTxr.process_record(session, rec)
        output = open(cheshirePath + '/cheshire3/dbs/istc/temp/data/' + istcNo + '.xml', 'w')
        output.write(doc.get_raw(session))
        output.flush()
        output.close()
missing035.write('</marc:collection>')
missing035.close()
manual035.close()
notInISTC.close()
missingShelf.close()

