"""Create XML version of bibliographic references data.

Originally used to clean create new bibliographical refs data when moving
from Cheshire 2 to Cheshire3 (June 2009)

Subsequently modified to create a more up-to-date copy of the XML data
following disaster recovery.

"""

import argparse
import re

from lxml import etree

from istcArguments import FileArgumentParser

# Init OptionParser
docbits = __doc__.split('\n\n')
arg_parser = FileArgumentParser(conflict_handler='resolve',
                                description=docbits[0]
                                )
arg_parser.set_defaults(infile="newBiblioData.txt",
                        outfile="../refsData/refs.xml"
                        )

args = arg_parser.parse_args()

lines = args.infile.readlines()
output = []

for l in lines:
    l = l.strip()
    if not l:
        continue
    toks = re.split('\s+', l, maxsplit=1)
    output.append('<record><code>%s</code><full>%s</full></record>' % (toks[0].replace('&', '&amp;').strip(), toks[1].replace('&', '&amp;').strip()))
    test = etree.fromstring('<refs>%s</refs>' % ''.join(output))
tree = etree.fromstring('<refs>%s</refs>' % ''.join(output))
parsedXslt = etree.parse("../xsl/reindent.xsl")
txr = etree.XSLT(parsedXslt)

result = txr(tree)

args.outfile.write(etree.tostring(result))
args.outfile.flush()
args.outfile.close()
