#!/usr/bin/env python3
import getopt
import sys

import parser
from coco_sdecb import keywords, remarks
from coco_util import getids, getidtype


class IDError(RuntimeError):
    pass


def nextid(prev):
    if len(prev) == 0:
        return 'A'
    if len(prev) == 1:
        if prev == 'Z':
            return 'A0'
        return chr(ord(prev) + 1)
    if prev == 'ZZ':
        raise IDError
    if prev[1] == '9':
        return prev[0] + 'A'
    if prev[1] == 'Z':
        return chr(ord(prev[0]) + 1) + '0'
    return prev[0] + chr(ord(prev[1]) + 1)


def getidmap(oldids, pp):
    newids = {}
    newid = ''
    for oldid in oldids:
        newid = nextid(newid)
        while newid in pp.kwtocode.keys():
            newid = nextid(newid)
        newids[oldid] = newid
    return newids


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-h\n')
    sys.stderr.write('\t--help\t\t\tthis help\n')
    sys.stderr.write('\t-i<iname>\n')
    sys.stderr.write('\t--input=<iname>\t\tinput file\n')
    sys.stderr.write('\t-o<oname>\n')
    sys.stderr.write('\t--output=<oname>\toutput file\n')


shortopts = 'hi:o:'
longopts = ["help", "input=", "output=", "start="]
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
        oname = f'{iname}.reid'
    else:
        oname = args[0]
        args = args[1:]

if len(args) != 0:
    usage()
    sys.exit(2)

pp = parser.Parser(keywords, remarks, open(iname, 'r').read())
oldids = getids(pp)
mymap = {}
for key in oldids.keys():
    mymap[key] = getidmap(oldids[key], pp)

data = pp.no_ws()

print(mymap)
for lix, line in enumerate(data):
    for tix, token in enumerate(line):
        if token[0] == parser.ID:
            data[lix][tix] = (parser.ID, mymap[getidtype(tix, line)][token[1]])

open(oname, 'w').write(pp.deparse(data))
