#!/usr/bin/env python3

from sys import argv

from basic69.coco import sdecb
from basic69 import Parser


class Options:
    keywords = sdecb.keywords
    remarks = sdecb.remarks
    disk = True
    isdragon = False

    def __init__(self):
        self.address = 0x0000


def main(args):
    for arg in args:
        with open(arg, "r") as fin:
            data = fin.read()
            parse_test(data)


def parse_test(data):
    opts = Options()
    pp = Parser(opts, data)
    for line in pp.full_parse:
        print(line)


if __name__ in "__main__":
    main(argv[1:])
