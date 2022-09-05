#!/usr/bin/env python3
import sys

from parser import Parser
from coco_dragon import options, dialect, tokenize


def main():
    usage = ('\t-c\t--cassette\t\tcasette file\n'
             '\t-d\t--disk\t\t\tdisk file (default)\n'
             '\t-w\t--whitespace\t\tpreserve whitespace\n')
    shortopts = 'cdw'
    longopts = ["cassette", "disk", "whitespace"]
    iname, oname, opts = options(sys.argv[1:], shortopts, longopts, usage, 'tok')
    ws = False
    disk = True
    for o, a in opts:
        if o in ["-c", "--casette"]:
            disk = False
        elif o in ["-d", "--disk"]:
            disk = True
        elif o in ["-w", "--whitespace"]:
            ws = True
        else:
            assert False, f'unhandled option [{o}]'
    pp = Parser(dialect, open(iname, 'r').read())
    open(oname, 'wb').write(tokenize(pp, ws=ws, disk=disk))


if __name__ == "__main__":
    main()
