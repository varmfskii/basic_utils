#!/usr/bin/env python3
import sys

from coco_dragon import Options, keywords, remarks, pack, tokenize
from parser import Parser


def main():
    usage = '\t-m\t--maxline=<num>\t\tmaximum tokenized line length\n'
    lopts = ["maxline="]
    opts = Options(sys.argv[1:], sopts='m:', lopts=lopts, usage=usage, ext='pack', astokens=True)
    maxline = 0
    for o, a in opts.unused:
        if o in ["-m", "--maxline"]:
            maxline = int(a)
            if maxline < 0:
                sys.stderr.write(f'length must be non-negative\n')
                sys.exit(2)
        else:
            assert False, f'unhandled option: [{o}]'
    pp = Parser(keywords, remarks, open(opts.iname, 'rb').read())
    pack(pp, maxline)
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp, disk=opts.disk))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
