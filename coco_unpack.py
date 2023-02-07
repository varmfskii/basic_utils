#!/usr/bin/env python3
import sys

from msbasic import splitlines
from basic69 import Options, Parser


def main():
    opts = Options(sys.argv[1:], ext='txt')
    for o, a in opts.unused:
        assert False, f'unhandled option: [{o}]'

    pp = Parser(opts, open(opts.iname, 'rb').read())
    splitlines(pp)
    open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
