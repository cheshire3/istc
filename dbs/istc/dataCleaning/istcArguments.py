
import argparse
import os
import sys

from argparse import ArgumentParser

# Cheshire3 imports
sys.path.insert(1, os.path.expanduser('~/cheshire3/code'))
from cheshire3.baseObjects import Session
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer


class UsageException(Exception):
    """UI Script usage exception."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ISTCArgumentParser(ArgumentParser):
    """Custom argument parser."""

    def __init__(self, **kwargs):
        ArgumentParser.__init__(self, **kwargs)


class FileArgumentParser(ISTCArgumentParser):
    """An ArgumentParser for process a file and produce output."""

    def __init__(self, **kwargs):
        ISTCArgumentParser.__init__(self, **kwargs)
        self.add_argument('infile',
                          nargs='?',
                          type=argparse.FileType('r'),
                          default=sys.stdin,
                          )
        self.add_argument('outfile',
                          nargs='?',
                          type=argparse.FileType('w'),
                          default=sys.stdout,
                          )


class DirectoryArgumentParser(ISTCArgumentParser):
    """An ArgumentParser for process whole directories at a time."""

    def __init__(self, **kwargs):
        ISTCArgumentParser.__init__(self, **kwargs)
        # Data Arguments
        group = self.add_argument_group("Data Options")
        group.add_argument(
            "-d", "--indir", dest="indd", default=os.path.join(dfp, 'data'), 
            help=" ".join(["Input data directory."]), 
            metavar="INDIR")
        group.add_argument(
            "-o", "--outdir", dest="outdd", default=os.path.join(dfp, 'data_new'), 
            help=" ".join(["Output data directory."]), 
            metavar="OUTDIR")


class BatchEditArgumentParser(DirectoryArgumentParser):

    def __init__(self, **kwargs):
        DirectoryArgumentParser.__init__(self, **kwargs)

        # Operation options
        group = self.add_mutually_exclusive_group()
        group.add_argument(
            "-s", "--strip",
            dest="strip", action='store_true', default=False,
            help=("Strip fields.")
        )
        group.add_argument(
            "-i", "--insert",
            dest="insert", action='store_true', default=False,
            help=("Insert fields.")
        )
        group.add_argument(
            "-r", "--replace",
            dest="replace", action='store_true', default=False,
            help=("Replace fields.")
        )

        # Debugging Arguments
        group3 = self.add_argument_group("Debug Options")
        group3.add_argument(
          "-t", "--test", action="store_true", dest="test",
          help="Carry out unit tests.")

        # Positional argument (transformation file name)
        self.add_argument(
            "transform",
            nargs='+',
            metavar="INPUTFILE",
            help=("Path to file containing data to strip/insert/replace")
        )

    def parse_args(self, args=None, namespace=None):
        args = ArgumentParser.parse_args(self, args, namespace)
        if args.test:
            return args

        ops = [args.strip,
               args.insert,
               args.replace]
        if not any(ops):
            # No operation specified
            msg = "operation must be given from: --strip, --insert, --replace"
            raise UsageException(msg)
        elif any(ops[1:]):
            if not args.transform:
                # Missing file argument for operation that requires it
                msg = "input file must be provided"
                raise UsageException(msg)
            for fn in args.transform:
                if not fn.endswith((".csv", ".xml", ".txt")):
                    msg = "unsupported INPUTFILE extension; must be one of: .csv .xml .txt"
                    raise UsageException(msg)
        return args


# Build environment...
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

session.database = 'db_istc'
db = serv.get_object(session, 'db_istc')
dfp = db.get_path(session, 'defaultPath')

