#!/usr/bin/env python3
import sys

import coco_util as cu
import parser


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
        while newid in pp.kw2code.keys():
            newid = nextid(newid)
        newids[oldid] = newid
    return newids


def usage():
    sys.stderr.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
    sys.stderr.write('\t-h\t--help\t\tthis help\n')
    sys.stderr.write('\t-i<n>\t--input=<file>\tinput file\n')
    sys.stderr.write('\t-o<n>\t--output=<file>\toutput file\n')


shortopts = ''
longopts = []
iname, oname, opts = cu.options(sys.argv[1:], '', [], usage, 'reid')

for o, a in opts:
    assert False, "unhandled option"

pp = parser.Parser(cu.keywords, cu.remarks, open(iname, 'r').read())
oldids = cu.getids(pp)
mymap = {}
for key in oldids.keys():
    mymap[key] = getidmap(oldids[key], pp)

data = pp.no_ws()

for lix, line in enumerate(data):
    for tix, token in enumerate(line):
        if token[0] == parser.ID:
            data[lix][tix] = (parser.ID, mymap[cu.getidtype(tix, line)][token[1].upper()])

open(oname, 'w').write(pp.deparse(data))
