#!/usr/bin/env python3

from sys import argv
from parser import Parser
from coco_dragon import sdecb

def main(args):
    for arg in args:
        with open(arg, "r") as fin:
            data = fin.read()
            parse_test(data)

def parse_test(data):
    pp = Parser(sdecb.keywords, sdecb.remarks, data)
    for line in pp.full_parse:
        print(line)
    
if __name__ in "__main__":
    main(argv[1:])
    
