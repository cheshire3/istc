#!/home/cheshire/install/bin/python -i
# -*- coding: iso-8859-1 -*-
"""Change wording of Microfiche data when moving from C2 to C3 (June 2009).

Usage: %prog [options] INPUTFILE

Options:
  -h, --help            show this help message and exit

  Data Options:
    -d INDIR, --indir=INDIR
                        Input data directory.
    -o OUTDIR, --outdir=OUTDIR
                        Output data directory.

  Operation Options:
    -s REPOSITORY, --strip=REPOSITORY
                        Strip facsimile copies for the specified repository.
    -i REPOSITORY, --insert=REPOSITORY
                        Insert facsimile copies for the specified repository.
    -r REPOSITORY, --replace=REPOSITORY
                        Replace facsimile copies for the specified repository.

  Debug Options:
    -t, --test          Carry out unit tests.


"""
from __future__ import with_statement

import sys
import os
import time
import csv

from optparse import OptionParser, OptionGroup

from lxml import etree

cheshirePath = "/home/cheshire"
sys.path.insert(1, os.path.join(cheshirePath, 'cheshire3', 'code'))

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument

# Configuration
aFieldStrings = {
    'darmstadt': """\
Electronic facsimile : Universit&#228;ts und Landesbibliothek Darmstadt""",
    'munich': """\
Electronic facsimile : Bayerische Staatsbibliothek, M&#252;nchen"""
}


class UsageException(Exception):
    """UI Script usage exception."""
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


class MyOptionParser(OptionParser):
    """Custom option parser for outputting list of record URIs."""
    
    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)
        # Data Options
        group = OptionGroup(self, "Data Options")
        group.add_option(
            "-d", "--indir", dest="indd", default=os.path.join(dfp, 'data'), 
            help=" ".join(["Input data directory."]), 
            metavar="INDIR")
        group.add_option(
            "-o", "--outdir", dest="outdd", default=os.path.join(dfp, 'data_new'), 
            help=" ".join(["Output data directory."]), 
            metavar="OUTDIR")
        self.add_option_group(group)
        # Operation Options
        group = OptionGroup(self, "Operation Options")
        group.add_option(
            "-s", "--strip", dest="strip", default=None, 
            help=" ".join(["Strip facsimile copies for the specified repository."]), 
            metavar="REPOSITORY")
        group.add_option(
            "-i", "--insert", dest="insert", default=None, 
            help=" ".join(["Insert facsimile copies for the specified repository."]), 
            metavar="REPOSITORY")
        group.add_option(
            "-r", "--replace", dest="replace", default=None, 
            help=" ".join(["Replace facsimile copies for the specified repository."]), 
            metavar="REPOSITORY")
        self.add_option_group(group)
        group3 = OptionGroup(self, "Debug Options")
        group3.add_option(
          "-t", "--test", action="store_true", dest="test",
          help="Carry out unit tests.")
        self.add_option_group(group3)
        
    def parse_args(self, args=None, values=None):
        (options, args) = OptionParser.parse_args(self, args, values)
        if options.test:
            return (options, args)
            
        ops = [options.strip,
               options.insert,
               options.replace]
        if not any(ops):
            # No operation specified
            msg = "operation must be given from: --strip, --insert, --replace"
            raise UsageException(msg)
        elif sum(int(bool(op)) for op in ops) > 1:
            # More than one operation specified
            msg = "only one operation can be given."
            raise UsageException(msg)
        elif any(ops[1:]):
            if not args:
                # Missing file argument for operation that requires it
                msg = "input file must be provided"
                raise UsageException(msg)
            elif not args[0].endswith((".csv", ".xml", ".txt")):
                msg = "unsupported INPUTFILE extension; must be one of: .csv .xml .txt"
                raise UsageException(msg)
        
        return (options, args)
        
                    
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
    bsbDict = {}
    incunab = xdoc.xpath('//incunabulum')
    for entry in incunab:
        BSBno = entry.xpath('./bsb-ink')[0].text
        if entry.xpath('./dig-art')[0].text == 'ZEND' or \
               entry.xpath('./dig-art')[0].text == 'Einblattdruck':
            uris = bsbDict.setdefault(BSBno, [])
            uris.append('http://mdzx.bib-bvb.de/bsbink/Ausgabe_%s.html' % BSBno)
    return bsbDict


def bsbDictFromText(filelike):
    """Construct and return dictionary of BSB no. to URI from text in file-like object."""
    bsbDict = {}
    for line in filelike.readlines():
        line = line.strip()
        try:
            foo, BSBno, uri = line.split()
        except ValueError:
            continue
        else:
            uris = bsbDict.setdefault(BSBno, [])
            uris.append(uri)
    return bsbDict
    

def bsbDictFromTextFile(filepath):
    """Construct and return dictionary of BSB no. to URI from text file at filepath."""
    with open(filepath, 'r') as fh:
        bsbDict = bsbDictFromText(fh)
    return bsbDict


# Functions / Methods for manipulating XML etrees
            
def stripFacsimileNodes(tree, repository):
    """Return the tree with matching 530 field nodes stripped out.
	
	tree			:= the etree to process
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
def strip(options, args):
    """Process files to remove 530 tags with the key words in them."""
    if options.strip is not None:
        repository = options.strip
    else:
        repository = options.replace
    for fn in os.listdir(options.indd):
        with open(os.path.join(options.indd, fn), 'r') as fh:
            targetTree = etree.parse(fh)
        targetTree = stripFacsimileNodes(targetTree, repository)
        doc = StringDocument(etree.tostring(targetTree))
        # parse and transform to prettily indent
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)
        # write output file
        outpath = os.path.join(options.outdd, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))
        print outpath, "stripped"
        

def insertSingle(options, fn, bsbDict):
    if options.insert is not None:
        repository = options.insert
    else:
        repository = options.replace
        
    with open(os.path.join(options.indd, fn), 'r') as fh:
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
        outpath = os.path.join(options.outdd, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))
        print outpath, "inserted"


def insert(options, args):
    """Process files to add the new ones from the datafile."""
    
    # Parse new data file
    newDataPath = os.path.join(dfp, 'dataCleaning', args[0])
    if newDataPath.endswith('.xml'):
        bsbDict = bsbDictFromXML(newDataPath)
    elif newDataPath.endswith('.txt'):
        bsbDict = bsbDictFromTextFile(newDataPath)
    elif newDataPath.endswith('.csv'):
        bsbDict = istcDictFromCsv(newDataPath)
        
    for fn in os.listdir(options.indd):
        insertSingle(options, fn, bsbDict)


def test():
    raise NotImplementedError


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        (options, args) = option_parser.parse_args(argv)
    except UsageException as err:
        option_parser.print_usage(file=sys.stderr)
        print >>sys.stderr, str(err)
        print >>sys.stderr, "for help use --help"
        return 1

    if options.test:
        test()
    elif options.strip is not None:
        strip(options, args)
    elif options.insert is not None:
        insert(options, args)
    elif options.replace is not None:
        strip(options, args)
        options.indd = options.outdd
        insert(options, args)
    return 0
    

# Build environment...
session = Session()
serv = SimpleServer(session, os.path.join(cheshirePath , 'cheshire3', 'configs', 'serverConfig.xml'))

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')
qf = db.get_object(session, 'defaultQueryFactory')
dfp = db.get_path(session, 'defaultPath')

# Init OptionParser
docbits = __doc__.split('\n\n')
option_parser = MyOptionParser(description=docbits[0], 
                      usage=docbits[1],
                      epilog=docbits[-1])


if __name__ == '__main__':
    sys.exit(main())
