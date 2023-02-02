#!/usr/bin/env python3
import sys

from coco_dragon import options, keywords, remarks, renumber
from parser import Parser


def main():
    usage = ('\t-s<n>\t--start=<num>\t\tstarting line number\n'
             '\t-v<n>\t--interval=<num>\tinterval between line numbers\n')
    shortopts = 's:v:'
    longopts = ["start=", "interval="]
    iname, oname, opts = options(sys.argv[1:], shortopts, longopts, usage, 'renum')
    start = 10
    interval = 10
    for o, a in opts:
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
    pp = Parser(keywords, remarks, open(iname, 'r').read())
    renumber(pp, start=start, interval=interval)
    open(oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
