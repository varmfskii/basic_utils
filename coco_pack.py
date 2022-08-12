#!/usr/bin/env python3
import sys

import coco_util as cu
import parser

usage = ('\t-c\t--casette\t\ttokenized cassette file\n'
         '\t-d\t--disk\t\t\ttokenized disk file (default)\n'
         '\t-u\t--text\t\t\ttext file\n')

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
