"""Add notes from a file into the ISTC database."""

import codecs
import os
import sys

from istcArguments import FileArgumentParser


from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.exceptions import ObjectDoesNotExistException
from cheshire3.server import SimpleServer
from cheshire3.internal import cheshire3Root

from istcArguments import FileArgumentParser


def main(argv=None):
    global arg_parser, notesStore
    if argv is not None:
        args = arg_parser.parse_args(argv)
    else:
        args = arg_parser.parse_args()
    for l in args.infile:
        # Check for Byte Order Mark
        if l.startswith(codecs.BOM_UTF8):
            l = l[3:]
        try:
            istc_no, notes = l.strip().split('\t', 1)
        except ValueError:
            continue
        try:
            doc = notesStore.fetch_document(session, istc_no)
        except ObjectDoesNotExistException:
            doc = StringDocument(notes)
        else:
            if notes != doc.get_raw(session):
                doc = StringDocument('{0}; {1}'.format(doc.get_raw(session),
                                                       notes
                                                       )
                                     )
        doc.id = istc_no
        notesStore.store_document(session, doc)

    return 0


# Init OptionParser
docbits = __doc__.split('\n\n')
arg_parser = FileArgumentParser(conflict_handler='resolve',
                                description=docbits[0]
                                )
arg_parser.set_defaults(infile="ISTCNotes.txt")

# Build environment...
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
notesStore = db.get_object(session, 'notesStore')

if __name__ == '__main__':
    sys.exit(main())
