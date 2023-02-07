#!/usr/bin/env python3
import sys

from coco_dragon import Options, keywords, remarks, splitlines, tokenize
from parser import Parser


def main():
    opts = Options(sys.argv[1:], ext='txt')
    for o, a in opts.unused:
        assert False, f'unhandled option: [{o}]'

    pp = Parser(keywords, remarks, open(opts.iname, 'rb').read())
    splitlines(pp)
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp, ws=True, disk=opts.disk))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
