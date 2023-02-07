from basic69.coco import cb, ecb, decb, secb, sdecb
from basic69.dragon import basic as dragon
from basic69.dragon import ddos
from msbasic.options import Options as BaseOptions
from msbasic.tokens import tokenize_line, detokenize_body
from .parser import Parser


class Options(BaseOptions):
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
    address = 0x2601

    def subopts(self, other):
        (o, a) = other
        dialects = {
            "cb": (cb.keywords, cb.remarks, False),
            "ecb": (ecb.keywords, ecb.remarks, False),
            "decb": (decb.keywords, decb.remarks, False),
            "secb": (secb.keywords, secb.remarks, False),
            "sdecb": (sdecb.keywords, sdecb.remarks, False),
            "dragon": (dragon.keywords, dragon.remarks, True),
            "ddos": (ddos.keywords, ddos.remarks, True),
        }
        if o in ["-b", "--basic"]:
            if a in dialects.keys():
                self.keywords, self.remarks, self.isdragon = dialects[a]
            elif a == "help":
                print("Supported dialects:")
                for key in dialects.keys():
                    print(f'\t{key}')
                sys.exit(0)
            else:
                sys.stderr.write(f'Unsupported dialect: {a}\n')
                sys.stderr.write("--basic=help to list available dialects")
                sys.exit(2)
        if o in ["-c", "--cassette"]:
            self.disk = False
            self.astokens = True
        elif o in ["-d", "--disk"]:
            self.disk = True
            self.astokens = True
        else:
            self.unused.append(other)

        if self.isdragon:
            self.address = 0x2401
        elif self.disk:
            self.address = 0x2601
        else:
            self.address = 0x25fe


def tokenize(pp, ws=False):
    # convert a parsed file into tokenized BASIC file
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    address = pp.address
    for line in parsed:
        line_tokens = tokenize_line(line, pp)
        address += 2 + len(line_tokens)
        tokenized += [address // 0x100, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if pp.isdragon:
        val = len(tokenized)
        tokenized = [0x55, 0x01, 0x24, 0x01, val // 256, val & 0xff, 0x8b, 0x8d, 0xaa] + tokenized
    elif pp.disk:
        val = len(tokenized)
        tokenized = [0xff, val // 0x100, val & 0xff] + tokenized
    return bytearray(tokenized)


def detokenize(opts, data):
    data = list(data)
    pp = Parser(opts)

    if data[0] == 0x55:
        ix = 9
        opts.keywords, opts.remarks = ddos.keywords, ddos.remarks
    elif data[0] == 0xff:
        ix = 3
        opts.keywords, opts.remarks = sdecb.keywords, sdecb.remarks
    else:
        ix = 0
        opts.keywords, opts.remarks = sdecb.keywords, sdecb.remarks

    return detokenize_body(data[ix:], pp)


if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
