#!/usr/bin/env python3
import sys

import coco_util as cu
import parser

usage = ''
shortopts = ''
longopts = []
iname, oname, opts = cu.options(sys.argv[1:], shortopts, longopts, usage, 'reid')

for o, a in opts:
    assert False, f'unhandled option [{o}]'

pp = parser.Parser(cu.keywords, cu.remarks, open(iname, 'r').read())
cu.reid(pp)
open(oname, 'w').write(pp.deparse(pp.full_parse))
