#!/usr/bin/env python3
import sys

from basic69 import Options, Parser


def main(args):
    opts = Options(args, ext='txt')

    for o, a in opts.unused:
        assert False, f'unhandled option [{o}]'

    pp = Parser(opts, open(opts.iname, 'rb').read())
    open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main(sys.argv[1:])
