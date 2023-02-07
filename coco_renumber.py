#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic import renumber


def main():
    usage = ('\t-s<n>\t--start=<num>\t\tstarting line number\n'
             '\t-v<n>\t--interval=<num>\tinterval between line numbers\n')
    lopts = ["start=", "interval="]
    opts = Options(sys.argv[1:], sopts='s:v:', lopts=lopts, usage=usage, ext='renum')
    start = 10
    interval = 10
    for o, a in opts.unused:
        if o in ["-s", "--start"]:
            start = int(a)
            if start < 0 or start > 32767:
                sys.stderr.write(f'Illegal starting line number: {start}\n')
                sys.exit(2)
        elif o in ["-v", "--interval"]:
            interval = int(a)
            if interval < 1:
                sys.stderr.write(f'Illegal line number interval: {interval}\n')
                sys.exit(2)
        else:
            assert False, "unhandled option"
    pp = Parser(opts, open(opts.iname, 'rb').read())
    renumber(pp, start=start, interval=interval)
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
