#!/usr/bin/env python3
import sys

from coco_dragon import Options, keywords, remarks, tokenize
from parser import Parser


def main():
    usage = '\t-w\t--whitespace\t\tdo not preserve whitespace\n'
    lopts = ["whitespace"]
    opts = Options(sys.argv[1:], sopts='w', lopts=lopts, usage=usage, ext='tok', astokens=True)
    ws = True
    for o, a in opts.unused:
        if o in ["-w", "--whitespace"]:
            ws = False
        else:
            assert False, f'unhandled option [{o}]'
    pp = Parser(keywords, remarks, open(opts.iname, 'rb').read())
    if opts.astokens:
        open(opts.oname, 'wb').write(tokenize(pp, ws=ws, disk=opts.disk))
    else:
        open(opts.oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
