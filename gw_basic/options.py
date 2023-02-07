import getopt
import sys

from .basica import keywords
from .basica import remarks

keywords = .basica.keywords
remarks = .basica.remarks
isdragon = False


class Options:
    astokens = True
    disk = True
    sopts = "b:cdhi:o:u"
    lopts = ["basic=", "cassette", "disk", "help", "input=", "output=", "text"]
    iname = None
    oname = None
    unused = []
    usage = ('\t-b\t--basic=<dialect>\tbasic dialect\n'
             '\t-c\t--casette\t\ttokenized cassette file\n'
             '\t-d\t--disk\t\t\ttokenized disk file (default)\n'
             '\t-h\t--help\t\t\tthis help\n'
             '\t-i<n>\t--input=<file>\t\tinput file\n'
             '\t-o<n>\t--output=<file>\t\toutput file\n'
             '\t-u\t--text\t\t\ttext file\n')

    def __init__(self, args, sopts='', lopts=None, usage='', ext='bas', astokens=True):
        # parse options for msbasic utils including globally available options
        if lopts is None:
            lopts = []
        global keywords
        global remarks
        global isdragon

        self.astokens = astokens
        self.sopts += sopts
        self.lopts += lopts
        self.usage += usage

        dialects = {
            "cb": (cb.keywords, cb.remarks, False),
            "ecb": (ecb.keywords, ecb.remarks, False),
            "decb": (decb.keywords, decb.remarks, False),
            "secb": (secb.keywords, secb.remarks, False),
            "sdecb": (sdecb.keywords, sdecb.remarks, False),
            "dragon": (dragon.keywords, dragon.remarks, False),
            "ddos": (ddos.keywords, ddos.remarks, False),
        }
        try:
            opts, args = getopt.getopt(args, self.sopts, self.lopts)
        except getopt.GetoptError as err:
            print(err)
            self.show_usage(sys.stderr)
            sys.exit(2)

        for o, a in opts:
            if o in ["-h", "--help:"]:
                self.show_usage(sys.stdout)
                sys.exit(0)
            elif o in ["-i", "--input"]:
                self.iname = a
            elif o in ["-o", "--output"]:
                self.oname = a
            elif o in ["-b", "--basic"]:
                if a in dialects.keys():
                    keywords, remarks, isdragon = dialects[a]
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
            elif o in ["-u", "--text"]:
                self.astokens = False
            else:
                self.unused.append((o, a))

        if self.iname is None:
            if len(args) == 0:
                self.show_usage(sys.stderr)
                sys.exit(2)
            self.iname = args[0]
            args = args[1:]

        if self.oname is None:
            if len(args) == 0:
                self.oname = f'{self.iname}.{ext}'
            else:
                self.oname = args[0]
                args = args[1:]

        if len(args) != 0:
            self.show_usage(sys.stderr)
            sys.exit(2)

    def show_usage(self, fh):
        fh.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n' + self.usage)
