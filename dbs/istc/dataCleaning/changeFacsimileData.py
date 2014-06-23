#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-
"""Change wording of Microfiche data when moving from C2 to C3 (June 2009).

Usage: %prog [options] INPUTFILE

Positional arguments:
  INPUTFILE             Path to file containing data to strip/insert/replace

Optional arguments:
  -h, --help            show this help message and exit
  -s, --strip           Strip fields.
  -i, --insert          Insert fields.
  -r, --replace         Replace fields.

Data Options:
  -d INDIR, --indir INDIR
                        Input data directory.
  -o OUTDIR, --outdir OUTDIR
                        Output data directory.

Debug Options:
  -t, --test            Carry out unit tests.

"""
from __future__ import with_statement

import sys
import os
import time
import csv

from collections import defaultdict

from lxml import etree


from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.server import SimpleServer
from cheshire3.internal import cheshire3Root

from istcArguments import BatchEditArgumentParser

# Configuration
aFieldStrings = {
    'darmstadt': """\
Electronic facsimile : Universit&#228;ts und Landesbibliothek Darmstadt""",
    'munich': """\
Electronic facsimile : Bayerische Staatsbibliothek, M&#252;nchen"""
}


# Functions / Methods for parsing input files

def istcDictFromCsv(filepath):
    """Construct and return a dictionary of ISTC no. to URI from CSV file at filepath."""
    istcDict = {}
    with open(filepath, 'r') as fh:
        csvr = csv.reader(fh)
        for uri, istcno in csvr:
            istcDict[istcno] = uri
    return istcDict


def bsbDictFromXML(filepath):
    """Construct and return a dictionary of BSB no. to URI from XML file at filepath."""
    with open(filepath, 'r') as fh:
        xdoc = etree.parse(fh)
    bsbDict = defaultdict(list)
    incunab = xdoc.xpath('//incunabulum')
    for entry in incunab:
        BSBno = entry.xpath('./bsb-ink')[0].text
        if entry.xpath('./dig-art')[0].text == 'ZEND' or \
               entry.xpath('./dig-art')[0].text == 'Einblattdruck':
            bsbDict[BSBno].append(
                'http://mdzx.bib-bvb.de/bsbink/Ausgabe_%s.html' % BSBno
            )
    return bsbDict


def bsbDictFromText(filelike):
    """Construct and return dictionary of BSB no. to URI from text in file-like object."""
    bsbDict = defaultdict(list)
    for line in filelike.readlines():
        line = line.strip()
        try:
            foo, BSBno, uri = line.split()
        except ValueError:
            continue
        else:
            bsbDict[BSBno].append(uri)
    return bsbDict


def bsbDictFromTextFile(filepath):
    """Construct and return dictionary of BSB no. to URI from text file at filepath."""
    with open(filepath, 'r') as fh:
        bsbDict = bsbDictFromText(fh)
    return bsbDict


# Functions / Methods for manipulating XML etrees

def stripFacsimileNodes(tree, repository):
    """Return the tree with matching 530 field nodes stripped out.

    tree            := the etree to process
    """
    parent = tree.xpath('/record')[0]
    for match in tree.xpath('//datafield[@tag="530"]'):
        sfnode = match.xpath('./subfield[@code="a"]')[0]
        if sfnode.text is None:
            pass
        else:
            sftext = sfnode.text.strip()
            sftext = sftext.lower()
            sftext = sftext.encode('ascii', 'xmlcharrefreplace')
            if 'electronic' in sftext:
                if sftext == aFieldStrings[repository].strip().lower():
                    parent.remove(match)
    return tree


# Functions / Method for main operations
def strip(args):
    """Process files to remove 530 tags with the key words in them."""
    if args.strip is not None:
        repository = args.strip
    else:
        repository = args.replace
    for fn in os.listdir(args.indd):
        with open(os.path.join(args.indd, fn), 'r') as fh:
            targetTree = etree.parse(fh)
        targetTree = stripFacsimileNodes(targetTree, repository)
        doc = StringDocument(etree.tostring(targetTree))
        # parse and transform to prettily indent
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)
        # write output file
        outpath = os.path.join(args.outdd, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))
        print outpath, "stripped"


def insertSingle(args, fn, bsbDict):
    if args.insert is not None:
        repository = args.insert
    else:
        repository = args.replace

    with open(os.path.join(args.indd, fn), 'r') as fh:
        targetTree = etree.parse(fh)
    istcno = os.path.splitext(fn)[0]
    parent = targetTree.xpath('/record')[0]
    try:
        urls = bsbDict[istcno]
    except KeyError:
        # Have to check BSB Numbers for Munich
        refs = targetTree.xpath('//datafield[@tag="510"]/subfield[@code="a"]')
        urls = None
        for ref in refs:
            if 'BSB-Ink' in ref.text:
                sf = ref.getparent()
                txt = etree.tostring(sf, method="text")
                BSBno = txt.split()[1]
                try:
                    urls = bsbDict[BSBno]
                except KeyError:
                    BSBno = '(%s)' % BSBno
                    try:
                        urls = bsbDict[BSBno]
                    except KeyError:
                        pass
    else:
        # Darmstadt file, simply maps ISTC no. to URL
        pass

    if urls is not None:
        # Process in reverse order, because insertSingleUrl will insert
        # new 530 field after final 510 field (i.e. before any existing
        # 530 fields.)
        for url in reversed(urls):
            # Create new 530 node
            datafield = etree.Element('datafield', tag='530', ind1='0', ind2='0')
            # Create subfield $a
            subfieldA = etree.Element('subfield', code='a')
            subfieldA.text = aFieldStrings[repository]
            datafield.append(subfieldA)
            # Create subfield $u
            subfieldU = etree.Element('subfield', code='u')
            subfieldU.text = url
            datafield.append(subfieldU)
            # Insert 530 field into parent after final 510 field
            last510 = targetTree.xpath('//datafield[@tag="510"]')[-1]
            parent.insert(parent.index(last510) + 1, datafield)
        dataString = etree.tostring(targetTree)
        dataString = dataString.replace('&amp;#', '&#')
        dataString = dataString.replace('&amp;amp;', '&amp;')
        doc = StringDocument(dataString)
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)
        # Write output file
        outpath = os.path.join(args.outdd, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))
        print outpath, "inserted"


def insert(args):
    """Process files to add the new ones from the datafile."""

    # Parse new data file
    newDataPath = os.path.join(dfp, 'dataCleaning', args[0])
    if newDataPath.endswith('.xml'):
        bsbDict = bsbDictFromXML(newDataPath)
    elif newDataPath.endswith('.txt'):
        bsbDict = bsbDictFromTextFile(newDataPath)
    elif newDataPath.endswith('.csv'):
        bsbDict = istcDictFromCsv(newDataPath)

    for fn in os.listdir(args.indd):
        insertSingle(args, fn, bsbDict)


def test():
    raise NotImplementedError


def main(argv=None):
    if argv is None:
        args = arg_parser.parse_args()
    else:
        args = arg_parser.parse_args(argv)

    if args.test:
        test()
    elif args.strip is not None:
        strip(args)
    elif args.insert is not None:
        insert(args)
    elif args.replace is not None:
        strip(args)
        args.indd = args.outdd
        insert(args)
    return 0


# Build environment...
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')
qf = db.get_object(session, 'defaultQueryFactory')
dfp = db.get_path(session, 'defaultPath')

# Init OptionParser
docbits = __doc__.split('\n\n')
arg_parser = BatchEditArgumentParser(description=docbits[0],
                                     epilog=docbits[-1]
                                     )


if __name__ == '__main__':
    sys.exit(main())
