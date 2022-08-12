#!/usr/bin/env python3
import sys

import coco as cu
import parser

usage = ('\t-c\t--cassette\t\tcasette file\n'
         '\t-d\t--disk\t\t\tdisk file (default)\n'
         '\t-w\t--whitespace\t\tpreserve whitespace\n')
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
