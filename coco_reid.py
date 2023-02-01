#!/usr/bin/env python3
import sys

from parser import Parser
from coco_dragon import options, keywords, remarks, reid


def main():
    usage = ''
    shortopts = ''
    longopts = []
    iname, oname, opts = options(sys.argv[1:], shortopts, longopts, usage, 'reid')
    for o, a in opts:
        assert False, f'unhandled option [{o}]'
    pp = Parser(keywords, remarks, open(iname, 'r').read())
    reid(pp)
    open(oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
