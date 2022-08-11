#!/usr/bin/env python3
import sys

import coco_util as cu
import parser


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-c\t--casette\ttokenized cassette file\n')
    sys.stderr.write('\t-d\t--disk\t\ttokenized disk file (default)\n')
    sys.stderr.write('\t-h\t--help\t\tthis help\n')
    sys.stderr.write('\t-i<n>\t--input=<file>\tinput file\n')
    sys.stderr.write('\t-o<n>\t--output=<file>\toutput file\n')
    sys.stderr.write('\t-u\t--text\t\ttext file\n')


disk = True
tokenize = True
shortopts = 'cdu'
longopts = ["cassette", "disk", "text"]
iname, oname, opts = cu.options(sys.argv[1:], shortopts, longopts, usage, 'pack')

for o, a in opts:
    if o in ["-c", "--cassette"]:
        disk = False
        tokenize = True
    elif o in ["-d", "--disk"]:
        disk = True
        tokenize = True
    elif o in ["-u", "--text"]:
        tokenize = False
    else:
        assert False, f'unhandled option: [{o}]'

pp = parser.Parser(cu.keywords, cu.remarks, open(iname, 'r').read())
cu.pack(pp)

if tokenize:
    open(oname, 'wb').write(cu.tokenize(pp, disk=disk))
else:
    open(oname, 'w').write(pp.deparse(pp.full_parse))
