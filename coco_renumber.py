#!/usr/bin/env python3
import getopt
import sys
import parser

from coco_util import renumber
from coco_sdecb import keywords, remarks


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-h\n')
    sys.stderr.write('\t--help\t\t\tthis help\n')
    sys.stderr.write('\t-i<iname>\n')
    sys.stderr.write('\t--input=<iname>\t\tinput file\n')
    sys.stderr.write('\t-o<oname>\n')
    sys.stderr.write('\t--output=<oname>\toutput file\n')
    sys.stderr.write('\t-s<start>\n')
    sys.stderr.write('\t--start=<start>\t\tstarting line number\n')
    sys.stderr.write('\t-v<interval>\n')
    sys.stderr.write('\t--interval=<interval>\t\tinverval between line numbers\n')


shortopts = 'hi:o:s:v:'
longopts = ["input=", "output=", "start=", "interval="]
try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

iname = None
oname = None
start = 10
interval = 10

for o, a in opts:
    if o in ["-h", "--help:"]:
        usage()
        sys.exit(0)
    elif o in ["-i", "--input"]:
        iname = a
    elif o in ["-o", "--output"]:
        oname = a
    elif o in ["-s", "--start"]:
        start = int(a)
        if start < 0 or start > 32767:
            sys.stderr.write(f'Illegal starting line number: {start}\n')
            sys.exit(2)
    elif o in ["-v", "--interval"]:
        interval = int(a)
        if interval < 1:
            sys.stderr.write(f'Illegal line number interval: {interval}\n')
            sys.exit(2)
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
        oname = f'{iname}.renum'
    else:
        oname = args[0]
        args = args[1:]

if len(args) != 0:
    usage()
    sys.exit(2)

pp = parser.Parser(keywords, remarks, open(iname, 'r').read())
renumber(pp, start=start, interval=interval)
open(oname, 'w').write(pp.deparse(pp.full_parse))
