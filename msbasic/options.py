import getopt
import sys


class Options:
    sopts = "a:hi:o:"
    lopts = ['address', "help", "input=", "output="]
    iname: str = None
    oname: str = None
    unused: [tuple[str, str]] = []
    address = 0
    dialects = {}
    usage = [
        '\t-a\t--address=<addy>\tstarting address\n',
        '\t-h\t--help\t\t\tthis help\n',
        '\t-i<n>\t--input=<file>\t\tinput file\n',
        '\t-o<n>\t--output=<file>\t\toutput file\n',
    ]
    keywords: [tuple[str, int]]

    def __init__(self, args: [str], sopts='', lopts: [str] = None, usage: [str] = None, ext='bas'):
        # parse options for msbasic utils including globally available options
        if not usage:
            usage = []
        if not lopts:
            lopts = []

        self.sopts += sopts
        self.lopts += lopts
        self.usage += usage

        try:
            opts, args = getopt.getopt(args, self.sopts, self.lopts)
        except getopt.GetoptError as err:
            print(err)
            self.show_usage(sys.stderr)
            sys.exit(2)

        for o, a in opts:
            if o in ['-a', '--address']:
                self.address = int(a)
            elif o in ["-b", "--basic"]:
                if a in self.dialects.keys():
                    self.dialect = self.dialects[a]()
                elif a == "help":
                    print("Supported dialects:")
                    for key in self.dialects.keys():
                        print(f'\t{key}:\t{self.dialects[key].numvar}')
                    sys.exit(0)
                else:
                    sys.stderr.write(f'Unsupported dialect: {a}\n')
                    sys.stderr.write("--basic=help to list available dialects")
                    sys.exit(2)
            elif o in ["-h", "--help:"]:
                self.show_usage(sys.stdout)
                sys.exit(0)
            elif o in ["-i", "--input"]:
                self.iname = a
            elif o in ["-o", "--output"]:
                self.oname = a
            else:
                self.subopts((o, a))

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

        self.post()

    def subopts(self, other: tuple[str, str]):
        self.unused.append(other)

    def post(self):
        pass

    def show_usage(self, fh):
        fh.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
        self.usage.sort()
        for line in self.usage:
            fh.write(line)
