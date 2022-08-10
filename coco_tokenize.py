#!/usr/bin/env python3
import getopt
import sys

from coco_util import tokenize_file


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-c\n')
    sys.stderr.write('\t--cassette\t\t\tcasette file\n')
    sys.stderr.write('\t-d\n')
    sys.stderr.write('\t--disk\t\t\tdisk file (default)\n')
    sys.stderr.write('\t-h\n')
    sys.stderr.write('\t--help\t\t\tthis help\n')
    sys.stderr.write('\t-i<iname>\n')
    sys.stderr.write('\t--input=<iname>\t\tinput file\n')
    sys.stderr.write('\t-o<oname>\n')
    sys.stderr.write('\t--output=<oname>\toutput file\n')
    sys.stderr.write('\t-w\n')
    sys.stderr.write('\t--whitespace\t\tpreserve whitespace\n')


shortopts = 'cdhi:o:w'
longopts = ["cassette", "disk", "input=", "output=", "whitespace"]
try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

iname = None
oname = None
ws = False
disk = True

for o, a in opts:
    if o in ["-c", "--casette"]:
        disk = False
    elif o in ["-d", "--disk"]:
        disk = True
    elif o in ["-h", "--help:"]:
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
    tokenize_file(iname, oname, ws=ws, disk=disk)
