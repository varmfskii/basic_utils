# parse Microsoft BASIC dialects, may be useful for some others
import re
import sys

from msbasic.parser import Parser as MSParser


class Parser(MSParser):
    def parse(self, data):
        if data[0] < 0x80 and data[1] < 0x80:
            data = "".join(map(chr, data))
            for line in re.split('[\n\r]+', data):
                parse = self.parse_line(line)
                if parse:
                    self.full_parse.append(parse)
        elif data[0] == 0xff:
            self.full_parse = self.parse_bin(data[3:])
        elif data[0] == 0x55:
            self.full_parse = self.parse_bin(data[9:])
        else:
            self.full_parse = self.parse_bin(data)


if __name__ == "__main__":
    sys.stderr.write("This is a library")
