#!/usr/bin/env python3
import sys

from coco_dragon import Options, keywords, remarks, reid, tokenize
from parser import Parser


def main():
    usage = ''
    shortopts = ''
    longopts = []
    opts = Options(sys.argv[1:], ext='reid')
    for o, a in opts.unused:
        assert False, f'unhandled option [{o}]'
    pp = Parser(keywords, remarks, open(opts.iname, 'rb').read())
    reid(pp)
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp, disk=opts.disk))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
