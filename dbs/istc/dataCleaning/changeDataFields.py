"""Change ISTC data.

Usage: %prog [options] INPUTFILE

Options:
  -h, --help            show this help message and exit

  Data Options:
    -d INDIR, --indir=INDIR
                        Input data directory.
    -o OUTDIR, --outdir=OUTDIR
                        Output data directory.

  Operation Options:
    -s, --strip
                        Strip fileds
    -i, --insert
                        Insert fields
    -r, --replace
                        Replace fields

  Debug Options:
    -t, --test          Carry out unit tests.


"""

import os
import sys

from lxml import etree

# Cheshire3 imports
sys.path.insert(1, os.path.expanduser('~/cheshire3/code'))
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.document import StringDocument

from istcArguments import ISTCArgumentParser

# Functions / Methods for parsing input files

def istcDictFromText(filelike):
    """Construct and return dictionary of ISTC no. to data fields."""
    istcDict = {}
    for line in filelike.readlines():
        line = line.strip()
        istcNo, data = line.split('\t', 1)
        data = tuple(data.split('\t'))
        fields = istcDict.setdefault(istcNo, [])
        fields.append(data)
    return istcDict
    

def istcDictFromTextFile(filepath):
    """Construct and return dictionary of ISTC no. to data fields."""
    with open(filepath, 'r') as fh:
        istcDict = istcDictFromText(fh)
    return istcDict


def replace(istcDict, args):
    """Process files to remove fields with the key words in them."""
    for fn in os.listdir(args.indd):
        istcNo = os.path.splitext(fn)[0]
        with open(os.path.join(args.indd, fn), 'r') as fh:
            targetTree = etree.parse(fh)
        parent = targetTree.xpath('/record')[0]
        try:
            fields = istcDict[istcNo]
        except KeyError:
            # Nothing to replace
            continue
        else:
            for field in fields:
                for match in targetTree.xpath('//datafield[@tag="{0}"]'.format(field[0])):
                    sfnode = match.xpath('./subfield[@code="a"]')[0]
                    if sfnode.text is None:
                        pass
                    else:
                        sftext = sfnode.text.strip()
                        if field[1] in sftext:
                            print sftext
                            for subfield in match:
                                match.remove(subfield)
                            # Create subfield $a
                            subfieldA = etree.Element('subfield', code='a')
                            subfieldA.text = field[1]
                            match.append(subfieldA)
                            # Create subfield $b
                            subfieldB = etree.Element('subfield', code='b')
                            subfieldB.text = field[2]
                            match.append(subfieldB)

        doc = StringDocument(etree.tostring(targetTree))
        # Parse and transform to prettily indent
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)
        # Write output file
        outpath = os.path.join(args.outdd, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))
        print outpath, "replaced"


def test():
    raise NotImplementedError


def main(argv=None):
    if argv is not None:
        args = argument_parser.parse_args(argv)
    else:
        args = argument_parser.parse_args()
    
    if args.test:
        return test()
        
    # Parse new data file
    istcDict = {}
    for newDataPath in args.transform:
        if newDataPath.endswith('.xml'):
            istcDict.update(istcDictFromXML(newDataPath))
        elif newDataPath.endswith('.txt'):
            istcDict.update(istcDictFromTextFile(newDataPath))
        elif newDataPath.endswith('.csv'):
            istcDict.update(istcDictFromCsv(newDataPath))


    if args.replace:
        return replace(istcDict, args)
    return 0


# Build environment...
session = Session()
serv = SimpleServer(session, os.path.expanduser('~/cheshire3/configs/serverConfig.xml'))

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')
qf = db.get_object(session, 'defaultQueryFactory')
dfp = db.get_path(session, 'defaultPath')

# Init OptionParser
docbits = __doc__.split('\n\n')
argument_parser = ISTCArgumentParser(description=docbits[0],
                                     epilog=docbits[-1])


if __name__ == '__main__':
    sys.exit(main())

