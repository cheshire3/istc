"""Add notes from a file into the ISTC database."""

import codecs
import os
import re
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
    # Assemble dictionary of notes
    istc_number_re = re.compile('i[a-z]\d{8}\s+')
    istc_notes = {}
    for l in args.infile:
        # Check for Byte Order Mark
        if l.startswith(codecs.BOM_UTF8):
            l = l[3:]
        if istc_number_re.match(l):
            # Start of a new ISTC number
            try:
                istc_no, notes = l.strip().split('\t', 1)
            except ValueError:
                continue
        else:
            notes = l
        try:
            istc_notes.setdefault(istc_no, []).append(notes)
        except NameError:
            continue

    # Make edits
    for istc_no, notes in istc_notes.iteritems():
        try:
            doc = notesStore.fetch_document(session, istc_no)
        except ObjectDoesNotExistException:
            doc = StringDocument('\n'.join(notes))
        else:
            # Try to avoid duplicating existing notes
            docstr = doc.get_raw(session)
            for line in reversed(notes):
                if docstr.endswith('; ' + line):
                    # Truncate existing notes
                    docstr = docstr[:len('; ' + line)]
            notes.insert(0, docstr)
            doc = StringDocument('\n'.join(notes))

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
