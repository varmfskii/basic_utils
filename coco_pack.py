#!/usr/bin/env python3
import sys

from basic69 import Options, Parser, tokenize
from msbasic.pack import pack


def main():
    usage = [
        "\t-k\t--token-len\t\tline length is for tokenized form\n",
        "\t-m\t--maxline=<num>\t\tmaximum line length\n",
        "\t-t\t--text\t\t\toutput as text file\n",
        "\t-x\t--text-len\t\tline length is for untokenized form\n"
    ]
    lopts = ['token-len', 'maxline=', 'text', 'text-len']
    astokens = True
    text_len = False
    opts = Options(sys.argv[1:], sopts='km:tx', lopts=lopts, usage=usage, ext='pack', astokens=True)
    max_len = 0
    for o, a in opts.unused:
        if o in ['-k', '--token-len']:
            text_len = False
        elif o in ['-m', '--maxline']:
            max_len = int(a)
            if max_len < 0:
                sys.stderr.write(f'length must be non-negative\n')
                sys.exit(2)
        elif o in ['-t', '--textfile']:
            astokens = False
        elif o in ['-x', '--text-len']:
            text_len = True
        else:
            assert False, f'unhandled option: [{o}]'
    pp = Parser(opts, open(opts.iname, 'rb').read())
    data = pack(pp, text_len=text_len, max_len=max_len)
    if astokens:
        open(opts.oname, 'wb').write(tokenize(data, opts))
    else:
        open(opts.oname, 'w').write(pp.deparse(data))


if __name__ == "__main__":
    main()
