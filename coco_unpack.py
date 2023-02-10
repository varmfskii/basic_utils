#!/usr/bin/env python3
import sys

from basic69 import Options, Parser
from msbasic.pack import splitlines


def main():
    lo = ["no-whitespace"]
    us = ["\t-n\t--no-whitespace\t\tdo not add extra whitespace\n"]
    opts = Options(sys.argv[1:], sopts='n', lopts=lo, usage=us, ext='txt')
    ws = True
    for o, a in opts.unused:
        if o in ['-n', '--no-whitespace']:
            ws = False
        else:
            assert False, f'unhandled option: [{o}]'

    pp = Parser(opts, open(opts.iname, 'rb').read())
    data = splitlines(pp.full_parse)
    open(opts.oname, 'w').write(pp.deparse(data, ws=ws))


if __name__ == "__main__":
    main()
