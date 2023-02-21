from basic69.coco import color, cb, ecb, decb, secb, sdecb
from basic69.dragon import dragon, ddos
from msbasic.options import Options as BaseOptions
from msbasic.tokens import tokenize_line
from .parser import Parser


class Options(BaseOptions):
    DIALECTS = {
        "cb": (cb.keywords, color.remarks, False),
        "ecb": (ecb.keywords, color.remarks, False),
        "decb": (decb.keywords, color.remarks, False),
        "secb": (secb.keywords, color.remarks, False),
        "sdecb": (sdecb.keywords, color.remarks, False),
        "dragon": (dragon.keywords, dragon.remarks, True),
        "ddos": (ddos.keywords, dragon.remarks, True),
    }
    disk = True
    sopts = "b:cd" + BaseOptions.sopts
    lopts = ["basic=", "cassette", "disk"] + BaseOptions.lopts
    usage = BaseOptions.usage + [
        '\t-b\t--basic=<dialect>\tbasic dialect\n',
        '\t-c\t--cassette\t\ttokenized cassette file\n',
        '\t-d\t--disk\t\t\ttokenized disk file (default)\n'
    ]

    keywords = sdecb.keywords
    remarks = sdecb.remarks
    isdragon = False

    def subopts(self, other):
        (o, a) = other
        if o in ["-b", "--basic"]:
            if a in self.DIALECTS.keys():
                self.keywords, self.remarks, self.isdragon = self.DIALECTS[a]
            elif a == "help":
                print("Supported self.DIALECTS:")
                for key in self.DIALECTS.keys():
                    print(f'\t{key}')
                sys.exit(0)
            else:
                sys.stderr.write(f'Unsupported dialect: {a}\n')
                sys.stderr.write("--basic=help to list available dialects")
                sys.exit(2)
        elif o in ["-c", "--cassette"]:
            self.disk = False
        elif o in ["-d", "--disk"]:
            self.disk = True
        else:
            self.unused.append(other)

    def post(self):
        if self.address == 0x0000:
            if self.isdragon:
                self.address = 0x2401
            elif self.disk:
                self.address = 0x2601
            else:
                self.address = 0x25fe


def tokenize(data, opts):
    # convert a parsed file into tokenized BASIC file
    tokenized = []
    address = opts.address
    for line in data:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 0x100, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if opts.disk and opts.isdragon:
        val = len(tokenized)
        tokenized = [0x55, 0x01, 0x24, 0x01, val // 256, val & 0xff, 0x8b, 0x8d, 0xaa] + tokenized
    elif opts.disk:
        val = len(tokenized)
        tokenized = [0xff, val // 0x100, val & 0xff] + tokenized
    return bytearray(tokenized)


if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
