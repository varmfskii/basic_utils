#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic.variables import reid


def main():
    astokens = True
    usage = ["\t-t\t--text\t\t\toutput as text file\n"]
    lopts = ["text"]
    opts = Options(sys.argv[1:], sopts='t', lopts=lopts, usage=usage, ext='reid')
    for o, a in opts.unused:
        if o in ['-t', '--text']:
            astokens = False
        else:
            assert False, f'unhandled option [{o}]'
    pp = Parser(opts, open(opts.iname, 'rb').read())
    data = reid(pp)
    if astokens:
        open(opts.oname, 'wb').write(tokenize(data, opts))
    else:
        open(opts.oname, 'w').write(pp.deparse(data))


if __name__ == "__main__":
    main()
