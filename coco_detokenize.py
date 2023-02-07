#!/usr/bin/env python3
import sys

from basic69 import Options
from msbasic import detokenize


def main(args):
    options = Options(args, ext='txt')

    for o, a in options.unused:
        assert False, f'unhandled option [{o}]'

    pp, listing = detokenize(open(options.iname, 'rb').read())
    open(options.oname, 'w').write(listing)


if __name__ == "__main__":
    main(sys.argv[1:])
