#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic import reid


def main():
    opts = Options(sys.argv[1:], ext='reid')
    for o, a in opts.unused:
        assert False, f'unhandled option [{o}]'
    pp = Parser(opts, open(opts.iname, 'rb').read())
    reid(pp)
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
