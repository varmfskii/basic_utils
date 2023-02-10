#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic.labels import renumber


def main():
    astokens = True
    usage = [
        '\t-s<n>\t--start=<num>\t\tstarting line number\n',
        '\t-t\t--text\t\t\toutput as text file\n',
        '\t-v<n>\t--interval=<num>\tinterval between line numbers\n'
    ]
    lopts = ["start=", "interval=", 'text']
    opts = Options(sys.argv[1:], sopts='s:tv:', lopts=lopts, usage=usage, ext='renum')
    start = 10
    interval = 10
    for o, a in opts.unused:
        if o in ["-s", "--start"]:
            start = int(a)
            if start < 0 or start > 32767:
                sys.stderr.write(f'Illegal starting line number: {start}\n')
                sys.exit(2)
        elif o in ['-t', '--text']:
            astokens = False
        elif o in ["-v", "--interval"]:
            interval = int(a)
            if interval < 1:
                sys.stderr.write(f'Illegal line number interval: {interval}\n')
                sys.exit(2)
        else:
            assert False, "unhandled option"
    pp = Parser(opts, open(opts.iname, 'rb').read())
    data = renumber(pp.full_parse, start=start, interval=interval)
    if astokens:
        open(opts.oname, 'wb').write(tokenize(data, opts))
    else:
        open(opts.oname, 'w').write(pp.deparse(data))


if __name__ == "__main__":
    main()
