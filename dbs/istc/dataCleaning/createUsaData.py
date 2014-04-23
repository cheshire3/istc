"""Create XML version of USA references data.

Originally used to create new USA location data when moving from
Cheshire 2 to Cheshire3 (June 2009).
"""

import sys

from lxml import etree

from istcArguments import FileArgumentParser

# Init OptionParser
docbits = __doc__.split('\n\n')
arg_parser = FileArgumentParser(conflict_handler='resolve',
                                description=docbits[0]
                                )
arg_parser.set_defaults(infile="usaData.txt",
                        outfile="../usaData/usaCodes.xml")


def main(argv=None):
    if argv is not None:
        args = arg_parser.parse_args(argv)
    else:
        args = arg_parser.parse_args()

    output = []

    for l in args.infile:
        try:
            code, location = l.strip().split('\t')
        except ValueError:
            continue
        output.append('<record><code>{0}</code><full>{1}</full></record>'
                      ''.format(code,
                                location.replace('&', '&amp;').strip()
                                )
                      )

    tree = etree.fromstring('<usa>%s</usa>' % ''.join(output))
    parsedXslt = etree.parse("../xsl/reindent.xsl")
    txr = etree.XSLT(parsedXslt)

    result = txr(tree)

    args.outfile.write(etree.tostring(result))
    args.outfile.flush()
    args.outfile.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())