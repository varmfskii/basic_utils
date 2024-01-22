# parse Microsoft BASIC dialects, may be useful for some others
import sys

from msbasic.parser import Parser as MSParser


class Parser(MSParser):
    __version__ = 'basic69 240122'

    @staticmethod
    def version():
        return [f'Parser:\t{Parser.__version__}']+MSParser.version()

    def parse(self, data: [int], fix_data=False, onepass=False) -> [[tuple[int, str] or tuple[int, str, int]]]:
        if data[0] == 0xff:  # decb
            self.full_parse = self.kws_bin(data[3:])
        elif data[0] == 0x55:  # ddos
            self.full_parse = self.kws_bin(data[9:])
        else:
            binary = False
            for d in data:
                if d == 0:
                    binary = True
                    break
            if binary:
                self.full_parse = self.kws_bin(data)
            else:
                self.full_parse = self.kws_txt(data)
        if onepass:
            return self.full_parse
        return self.get_tokens(fix_data=fix_data)


if __name__ == "__main__":
    sys.stderr.write("This is a library")
