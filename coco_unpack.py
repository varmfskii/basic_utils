#!/usr/bin/env python3
import sys

from basic69 import Options, Parser
from msbasic import splitlines


def main():
    lo = ["no-whitespace"]
    us = "\t-n\t--no-whitespace\tDon't add extra whitespace\n"
    opts = Options(sys.argv[1:], sopts='n', lopts=lo, usage=us, ext='txt')
    ws = True
    for o, a in opts.unused:
        if o in ['-n', '--no-whitespace']:
            ws = False
        else:
            assert False, f'unhandled option: [{o}]'

    pp = Parser(opts, open(opts.iname, 'rb').read())
    splitlines(pp)
    open(opts.oname, 'w').write(pp.deparse(ws=ws))


if __name__ == "__main__":
    main()
