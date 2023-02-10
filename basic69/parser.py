# parse Microsoft BASIC dialects, may be useful for some others
import sys

from msbasic.parser import Parser as MSParser


class Parser(MSParser):

    def parse(self, data: list[int]) -> list[list[tuple]]:
        if data[0] < 0x80 and data[1] < 0x80:
            self.full_parse = self.parse_txt("".join(map(chr, data)))
        elif data[0] == 0xff:
            self.full_parse = self.parse_bin(data[3:])
        elif data[0] == 0x55:
            self.full_parse = self.parse_bin(data[9:])
        else:
            self.full_parse = self.parse_bin(data)
        return self.full_parse


if __name__ == "__main__":
    sys.stderr.write("This is a library")
