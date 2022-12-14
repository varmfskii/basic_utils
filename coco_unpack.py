#!/usr/bin/env python3
import sys

from coco_dragon import options, dialect, splitlines
from parser import Parser


def main():
    usage = ''
    shortopts = ''
    longopts = []
    iname, oname, opts = options(sys.argv[1:], shortopts, longopts, usage, 'txt')
    for o, a in opts:
        assert False, f'unhandled option: [{o}]'

    pp = Parser(dialect, open(iname, 'r').read())
    splitlines(pp)
    open(oname, 'w').write(pp.deparse(ws=True))


if __name__ == "__main__":
    main()
