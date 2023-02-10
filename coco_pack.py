#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic.pack import pack


def main():
    usage = [
        "\t-m\t--maxline=<num>\t\tmaximum tokenized line length\n",
        "\t-t\t--text\t\t\toutput as text file\n"
    ]
    lopts = ["maxline=", "text"]
    astokens = True
    opts = Options(sys.argv[1:], sopts='m:t', lopts=lopts, usage=usage, ext='pack', astokens=True)
    maxline = 0
    for o, a in opts.unused:
        if o in ["-m", "--maxline"]:
            maxline = int(a)
            if maxline < 0:
                sys.stderr.write(f'length must be non-negative\n')
                sys.exit(2)
        elif o in ['-t', '--textfile']:
            astokens = False
        else:
            assert False, f'unhandled option: [{o}]'
    pp = Parser(opts, open(opts.iname, 'rb').read())
    data = pack(pp, maxline)
    if astokens:
        open(opts.oname, 'wb').write(tokenize(data, opts))
    else:
        open(opts.oname, 'w').write(pp.deparse(data))


if __name__ == "__main__":
    main()
