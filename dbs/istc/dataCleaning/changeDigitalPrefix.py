# -*- coding: iso-8859-1 -*-
"""Change URLs for Microfiche data.

Positional arguments:
  match                 Regex to match against the content of the 530$u
                        field.Default is to match anything.

  replace               Replace value for the match in the 530$u field.
                        Default is empty string, i.e. strip the match

Optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Carry out unit tests.

Data Options:
  -d INDIR, --indir INDIR
                        Input data directory.
  -o OUTDIR, --outdir OUTDIR
                        Output data directory.

"""

import logging
import os
import re
import sys

# site-packages
from lxml import etree


from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.server import SimpleServer
from cheshire3.internal import cheshire3Root

from istcArguments import DirectoryArgumentParser


class MyArgParser(DirectoryArgumentParser):
    """Custom argument parser for changing field value prefix."""

    def __init__(self, **kwargs):
        DirectoryArgumentParser.__init__(self, **kwargs)
        # Operations
        """
        group = self.add_argument_group(title="Operations")
        group.add_argument(
            "-s", "--strip",
            dest="strip", default=None,
            metavar="REPOSITORY",
            help=("Strip facsimile copies for the specified repository"),
        )
        group.add_argument(
            "-i", "--insert",
            dest="insert", default=None, 
            metavar="REPOSITORY",
            help=("Insert facsimile copies for the specified repository.")
        )
        group.add_argument(
            "-r", "--replace",
            dest="replace", default=None,
            metavar="REPOSITORY",
            help=("Replace facsimile copies for the specified repository.")
        )
        """

        # Debug options
        self.add_argument(
            "-t", "--test", action="store_true", dest="test",
            help="Carry out unit tests."
        )
        # Positional arguments
        self.add_argument(
            "match",
            default=".*",
            help=("Regex to match against the content of the 530$u field."
                  "Default is to match anything."
            ),
        )
        self.add_argument(
            "replace",
            nargs='?',
            default="",
            help=("Replace value for the match in the 530$u field. "
                  "Default is empty string, i.e. strip the match"
                  )
        )


def replace(args):
    global dfp, parser
    aFieldRe = re.compile(args.match.strip(), re.I)
    for fn in os.listdir(args.indir):
        inpath = os.path.join(args.indir, fn)
        with open(inpath, 'r') as fh:
            tree = etree.parse(fh)
        parent = tree.xpath('/record')[0]
        for node in tree.xpath('//datafield[@tag="530"]/subfield[@code="u"]'):
            if node.text is None:
                continue
            elif aFieldRe.match(node.text.strip()):
                logging.debug(node.text.strip())
                sftext = aFieldRe.sub(args.replace, node.text.strip())
                node.text = sftext
                logging.debug(node.text.strip())
                logging.info("Modified {0}".format(inpath))
        
        doc = StringDocument(etree.tostring(tree))
        # parse and transform to prettily indent
        rec = parser.process_document(session, doc)
        doc2 = indentingTxr.process_record(session, rec)
        # write output file
        outpath = os.path.join(args.outdir, fn)
        with open(outpath, 'w') as outfh:
            outfh.write(doc2.get_raw(session))

    return 0


def main(argv=None):
    global argparser
    global session, server, db
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    return replace(args)


# Build environment...
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
dfp = db.get_path(session, 'defaultPath')
indentingTxr = db.get_object(session, 'indentingTxr')
parser = db.get_object(session, 'LxmlParser')

# Init OptionParser
docbits = __doc__.split('\n\n')
argparser = MyArgParser(conflict_handler='resolve',
                        description=docbits[0]
                        )

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s\t%(message)s'
                    )

if __name__ == '__main__':
    sys.exit(main())

