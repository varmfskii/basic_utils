import sys

from commodore import atbasic, simons, speech, superbasic, turtle
from commodore import base, basic4, basic10, basic35, c64_4, c128

from msbasic.options import Options as BaseOptions


class Options(BaseOptions):
    sopts = 'b:' + BaseOptions.sopts
    lopts = ['basic='] + BaseOptions.lopts
    usage = ['\t-b<d>\t--basic=<dialect>\tbasic dialect\n'] + BaseOptions.usage
    keywords = base.keywords
    remarks = base.remarks

    def subopts(self, other):
        o, a = other
        dialects = {
            "1.0": (base.keywords, base.remarks),
            "2.0": (base.keywords, base.remarks),
            "3.5": (basic35.keywords, base.remarks),
            "4.0": (basic4.keywords, base.remarks),
            "7.0": (c128.keywords, base.remarks),
            "10.0": (basic10.keywords, base.remarks),
            "pet": (base.keywords, base.remarks),
            "vic20": (base.keywords, base.remarks),
            "c64": (base.keywords, base.remarks),
            "c128": (c128.keywords, base.remarks),
            "c64_4.0": (c64_4.keywords, base.remarks),
            "super": (superbasic.keywords, base.remarks),
            "simons": (simons.keywords, base.remarks),
            "speech": (speech.keywords, base.remarks),
            "atbasic": (atbasic.keywords, base.remarks),
            "turtle": (turtle.keywords, base.remarks),
        }

        if o in ["-b", "--basic"]:
            if a in dialects.keys():
                self.keywords, self.remarks = dialects[a]
            elif a == "help":
                print("Supported dialects:")
                for key in dialects.keys():
                    print(f'\t{key}')
                sys.exit(0)
            else:
                sys.stderr.write(f'Unsupported dialect: {a}\n')
                sys.stderr.write("--basic=help to list available dialects")
                sys.exit(2)
        else:
            self.unused.append((o, a))


if __name__ == "__main__":
    sys.stderr.write("This is a library")
