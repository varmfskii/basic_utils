#!/usr/bin/env python3
import sys

import coco_util as cu
import parser


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-c\t--cassette\tcasette file\n')
    sys.stderr.write('\t-d\t--disk\t\tdisk file (default)\n')
    sys.stderr.write('\t-h\t--help\t\tthis help\n')
    sys.stderr.write('\t-i<n>\t--input=<file>\tinput file\n')
    sys.stderr.write('\t-o<n>\t--output=<file>\toutput file\n')
    sys.stderr.write('\t-w\t--whitespace\tpreserve whitespace\n')


shortopts = 'cdw'
longopts = ["cassette", "disk", "whitespace"]
iname, oname, opts = cu.options(sys.argv[1:], shortopts, longopts, usage, 'tok')
ws = False
disk = True

for o, a in opts:
    if o in ["-c", "--casette"]:
        disk = False
    elif o in ["-d", "--disk"]:
        disk = True
    elif o in ["-w", "--whitespace"]:
        ws = True
    else:
        assert False, f'unhandled option [{o}]'

pp = parser.Parser(cu.keywords, cu.remarks, open(iname, 'r').read())
open(oname, 'wb').write(cu.tokenize(pp, ws=ws, disk=disk))
