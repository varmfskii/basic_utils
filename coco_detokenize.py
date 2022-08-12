#!/usr/bin/env python3
import sys

from coco import options, detokenize


def main(args):
    usage = ''
    shortopts = ''
    longopts = []
    iname, oname, opts = options(args, shortopts, longopts, usage, 'txt')

    for o, a in opts:
        assert False, f'unhandled option [{o}]'

    pp, listing = detokenize(open(iname, 'rb').read())
    open(oname, 'w').write(listing)


if __name__ == "__main__":
    main(sys.argv[1:])
