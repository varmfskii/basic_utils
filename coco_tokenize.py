#!/usr/bin/env python3
import getopt
import sys

from coco_util import tokenize_file


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-h\n')
    sys.stderr.write('\t--help\t\t\tthis help\n')
    sys.stderr.write('\t-i<iname>\n')
    sys.stderr.write('\t--input=<iname>\t\tinput file\n')
    sys.stderr.write('\t-o<oname>\n')
    sys.stderr.write('\t--output=<oname>\toutput file\n')
    sys.stderr.write('\t-w\n')
    sys.stderr.write('\t--whitespace\t\tpreserve whitespace\n')


try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:w', ["input=", "output=", "whitespace"])
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

iname = None
oname = None
ws = False

for o, a in opts:
    if o in ["-h", "--help:"]:
        usage()
        sys.exit(0)
    elif o in ["-i", "--input"]:
        iname = a
    elif o in ["-o", "--output"]:
        oname = a
    elif o in ["-w", "--whitespace"]:
        ws = True
    else:
        assert False, "unhandled option"

if iname is None:
    if len(args) == 0:
        usage()
        sys.exit(2)
    iname = args[0]
    args = args[1:]

if oname is None:
    if len(args) == 0:
        oname = f'{iname}.tok'
    else:
        oname = args[0]
        args = args[1:]

if len(args) != 0:
    usage()
    sys.exit(2)

for fname in sys.argv[1:]:
    tokenize_file(iname, oname, ws=ws)
