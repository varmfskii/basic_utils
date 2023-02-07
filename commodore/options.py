import sys

from msbasic import options
from commodore import c64, c128


class Options(options.Options):
    sopts = "b:hi:o:u"
    lopts = ["basic=", "help", "input=", "output=", "text"]
    usage = ('\t-b\t--basic=<dialect>\tbasic dialect\n'
             '\t-h\t--help\t\t\tthis help\n'
             '\t-i<n>\t--input=<file>\t\tinput file\n'
             '\t-o<n>\t--output=<file>\t\toutput file\n'
             '\t-u\t--text\t\t\ttext file\n')
    keywords = c64.keywords
    remarks = c64.remarks

    def subopts(self, other):
        o, a = other
        dialects = {
            "64": (c64.keywords, c64.remarks),
            "128": (c128.keywords, c128.remarks),
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
