import sys

from msbasic.options import Options as BaseOptions
from msbasic.tokens import tokenize as mstokenize
from .dialects import DIALECTS, SDECB
from .parser import Parser


class Options(BaseOptions):
    __version__ = 'basic69 20240122'
    disk = None
    isdragon = False
    sopts = "cd" + BaseOptions.sopts
    lopts = ["cassette", "disk"] + BaseOptions.lopts
    usage = BaseOptions.usage + [
        '\t-c\t--cassette\t\ttokenized cassette file\n',
        '\t-d\t--disk\t\t\ttokenized disk file (default)\n'
    ]

    dialect = None
    dialects = DIALECTS

    def subopts(self, other):
        (o, a) = other
        if o in ["-c", "--cassette"]:
            self.disk = False
        elif o in ["-d", "--disk"]:
            self.disk = True
        else:
            self.unused.append(other)

    def post(self):
        if self.dialect is None:
            self.dialect = SDECB()
        if self.disk is None:
            self.disk = self.dialect.disk
        self.isdragon = self.dialect.dragon
        if self.address == 0x0000:
            if self.dialect.dragon:
                self.address = 0x2401
            elif self.disk:
                self.address = 0x2601
            else:
                self.address = 0x25fe


def tokenize(data, opts):
    # convert a parsed file into tokenized BASIC file
    tokenized = mstokenize(data, opts) + [0, 0]
    if opts.disk and opts.isdragon:
        val = len(tokenized)
        tokenized = [0x55, 0x01, 0x24, 0x01, val // 256, val & 0xff, 0x8b, 0x8d, 0xaa] + tokenized
    elif opts.disk:
        val = len(tokenized)
        tokenized = [0xff, val // 0x100, val & 0xff] + tokenized
    return bytearray(tokenized)


if __name__ == "__main__":
    sys.stderr.write("This is a library")
