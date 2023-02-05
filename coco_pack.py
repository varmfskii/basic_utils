#!/usr/bin/env python3
import sys

from coco_dragon import options, keywords, remarks, pack, tokenize
from parser import Parser


def main():
    usage = ('\t-c\t--casette\t\ttokenized cassette file\n'
             '\t-d\t--disk\t\t\ttokenized disk file (default)\n'
             '\t-u\t--text\t\t\ttext file\n')
    disk = True
    astokens = True
    shortopts = 'cdu'
    longopts = ["cassette", "disk", "text"]
    iname, oname, opts = options(sys.argv[1:], shortopts, longopts, usage, 'pack')
    for o, a in opts:
        if o in ["-c", "--cassette"]:
            disk = False
            astokens = True
        elif o in ["-d", "--disk"]:
            disk = True
            astokens = True
        elif o in ["-u", "--text"]:
            astokens = False
        else:
            assert False, f'unhandled option: [{o}]'
    pp = Parser(keywords, remarks, open(iname, 'rb').read())
    pack(pp)
    if astokens:
        open(oname, 'wb').write(tokenize(pp, disk=disk))
    else:
        open(oname, 'w').write(pp.deparse())


if __name__ == "__main__":
    main()
