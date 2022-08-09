#!/usr/bin/env python3
import sys

import parser


def parse_file(fname, keywords, remarks):
    fh = open(fname, 'r')
    lines = fh.read().split('\n')
    fh.close()
    pp = parser.Parser(keywords, remarks)
    for line in lines:
        pp.parse_line(line)
    return pp.pack()


keywords = []
remarks = []
exec(open("coco_sdecb.py").read())
for fname in sys.argv[1:]:
    parsed = parse_file(fname, keywords, remarks)
    print(parsed)
