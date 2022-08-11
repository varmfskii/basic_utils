#!/usr/bin/env python3
import sys

import coco_util as cu


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-h\t--help\t\tthis help\n')
    sys.stderr.write('\t-i<n>\t--input=<file>\tinput file\n')
    sys.stderr.write('\t-o<n>\t--output=<file>\toutput file\n')


shortopts = ''
longopts = []
iname, oname, opts = cu.options(sys.argv[1:], shortopts, longopts, usage, 'tok')
ws = False
disk = True

for o, a in opts:
    assert False, f'unhandled option [{o}]'

pp = cu.detokenize(open(iname, 'rb').read())
open(oname, 'wb').write(pp.deparse(pp.full_parse))
