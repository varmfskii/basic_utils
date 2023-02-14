import getopt
import sys

keywords = []
remarks = []


class Options:
    disk = True
    sopts = "a:hi:o:"
    lopts = ['address', "help", "input=", "output="]
    iname = None
    oname = None
    unused = []
    address = 0
    usage = [
        '\t-a\t--address=<addy>\t\t\tstarting address\n',
        '\t-h\t--help\t\t\tthis help\n',
        '\t-i<n>\t--input=<file>\t\tinput file\n',
        '\t-o<n>\t--output=<file>\t\toutput file\n',
    ]
    keywords = []
    remarks = []

    def __init__(self, args, sopts='', lopts=None, usage=None, ext='bas'):
        # parse options for msbasic utils including globally available options
        if usage is None:
            usage = []
        if lopts is None:
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

    def subopts(self, other):
        self.unused.append(other)

    def post(self):
        pass
    
    def show_usage(self, fh):
        fh.write(f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n')
        self.usage.sort()
        for line in self.usage:
            fh.write(line)
