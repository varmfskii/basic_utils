#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize


def main():
    opts = Options(sys.argv[1:], ext='tok')
    for o, a in opts.unused:
        assert False, f'unhandled option [{o}]'
    pp = Parser(opts, open(opts.iname, 'rb').read())
    open(opts.oname, 'wb').write(tokenize(pp.full_parse, opts))


if __name__ == "__main__":
    main()
