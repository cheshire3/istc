from lxml import etree
import os, re
from cheshire3.document import StringDocument
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
cheshirePath = "/home/cheshire"

# Build environment...
session = Session()
serv = SimpleServer(session, cheshirePath + "/cheshire3/configs/serverConfig.xml")

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')

datafile = open('GW2009-11-24.xml', 'r')

datatree = etree.fromstring(datafile.read())

items = datatree.xpath('//item')

gwdict = {}

for i in items:
    
    istcno = i.xpath('@ISTC')[0][:10]
    gwno = i.xpath('@GW')[0]
    index = 0
    if len(gwno) == 5:
        naught = True        
        for letter in gwno:
            if letter == '0':
                index += 1
            else:
                naught = False
                break 
    if gwno.find('Sp.') != -1:
        newgwno = []
        gwno = gwno.split(' ')
        if gwno[0] == '1':
            newgwno.append('I ')
        elif gwno[0] == '2':
            newgwno.append('II ')    
        elif gwno[0] == '3':
            newgwno.append('III ')    
        elif gwno[0] == '4':
            newgwno.append('IV ')
        elif gwno[0] == '5':
            newgwno.append('V ')
        elif gwno[0] == '6':
            newgwno.append('VI ')
        elif gwno[0] == '7':
            newgwno.append('VII ')
        elif gwno[0] == '8':
            newgwno.append('VIII ')
        elif gwno[0] == '9':
            newgwno.append('IX ')
        elif gwno[0] == '10':
            newgwno.append('X ')
        elif gwno[0] == '11':
            newgwno.append('XI ')
        newgwno.append('Sp.')
        try: 
            newgwno.append(gwno[2])
        except:
            newgwno.append(gwno[1][3:])
        gwno = ''.join(newgwno)
    try :
        gwdict[istcno].append(gwno[index:])
    except:
        gwdict[istcno] = [gwno[index:]]
        
        

dir = '/home/cheshire/cheshire3/dbs/istc/data/'

noNewEntries = []
twoNumbers = {}
complicatedOnes = {}
for f in os.listdir(dir):
    file = open(dir + f, 'r')   
    targetTree = etree.fromstring(file.read())
    file.close()
    parent = targetTree.xpath('/record')[0]
    istcno = targetTree.xpath('//controlfield[@tag="001"]/text()')[0]
    f510 = targetTree.xpath('//datafield[@tag="510"]')
    gwentries = None
    bracketText = {}
    entry = {}
   
    # cycle through 510 fields if they are GW numbers
    for field in f510:
        if field.xpath('./subfield[@code="a"]/text()')[0] == 'GW':
            text = field.xpath('./subfield[@code="c"]/text()')[0]
            regex1 = re.compile('^\S+(\s+\([^\)]*\))+$')
            regex2 = re.compile('^\S+\s+(\([^\)]+\)\s+)?\(([^\(\)]*\([^\)\(]*\)[^\)\(]*)+\)(\s+\([^\)]+\))?$')
            regex3 = re.compile('^[IV]+\scol\s[0-9]+(\s+\([^\)]*\))+$')
            if re.match(regex1, text) != None:
                bracketText[text[:text.find('(')-1]] = text[text.find('('):]
            elif re.match(regex2, text) != None:
                bracketText[text[:text.find('(')-1]] = text[text.find('('):]
            elif re.match(regex3, text) != None:
                bracketText[text[:text.find('(')-1].replace('col ', 'Sp.')] = text[text.find('('):]
            elif text.find('(') != -1:
                entry[text[:text.find('(')-1]] = text[text.find('('):]
                complicatedOnes[f] = entry
            elif text.find('=') != -1: 
                twoNumbers[istcno] = text
            elif text.find('+') != -1: 
                twoNumbers[istcno] = text
            elif text.find('&') != -1: 
                twoNumbers[istcno] = text
            elif text.find(',') != -1: 
                twoNumbers[istcno] = text
            try:
                gwentries = gwdict[istcno]
            except:
                if istcno not in noNewEntries:
                    noNewEntries.append(istcno)
            else:
                parent.remove(field)
    try: gwdict[istcno]
    except: pass
    else:
        for gw in gwdict[istcno]:
            datafield = etree.Element('datafield', tag='510', ind1='4', ind2=' ')
            subfieldA = etree.Element('subfield', code='a')
            subfieldA.text = 'GW'
            subfieldC = etree.Element('subfield', code='c')
            try:
                extra = bracketText[gw]
            except:
                extra = ''
            else:
                bracketText[gw] = None
            if extra != '':
                subfieldC.text = '%s %s' % (gw, extra)
            else:
                subfieldC.text = gw
            datafield.append(subfieldA)
            datafield.append(subfieldC)
            
            if targetTree.xpath('//datafield[@tag="510"]'):
            
                last510 = targetTree.xpath('//datafield[@tag="510"]')[-1]
                
                if last510.xpath('./subfield[@code="a"]/text()')[0].find('Fac') == 0:
                    parent.insert(targetTree.index(last510), datafield) 
                else:
                    parent.insert(targetTree.index(last510) + 1, datafield)  
            elif targetTree.xpath('//datafield[@tag="300"]'):
                last300 = targetTree.xpath('//datafield[@tag="300"]')[-1]
                parent.insert(targetTree.index(last300) + 1, datafield)
            else:
                last260 = targetTree.xpath('//datafield[@tag="260"]')[-1]
                parent.insert(targetTree.index(last260) + 1, datafield)
            for b in bracketText.keys():
                if bracketText[b] != None:
                    print istcno,
                    print ' %s ' % b,
                    print bracketText[b]

    
        doc = StringDocument(etree.tostring(targetTree))
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec) 
        output = open(cheshirePath + '/cheshire3/dbs/istc/data/' + f + '.xml', 'w')
        output.write(doc2.get_raw(session))
        output.flush()
        output.close()
        
print complicatedOnes
print noNewEntries
print twoNumbers