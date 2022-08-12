#!/usr/bin/env python3
import sys

import coco_util as cu

usage = ''
shortopts = ''
longopts = []
iname, oname, opts = cu.options(sys.argv[1:], shortopts, longopts, usage, 'txt')
ws = False
disk = True

for o, a in opts:
    assert False, f'unhandled option [{o}]'

pp, listing = cu.detokenize(open(iname, 'rb').read())
open(oname, 'w').write(listing)
