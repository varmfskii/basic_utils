import getopt
import sys

from coco_dragon.coco_basic import cb, ecb, decb, secb, sdecb
from coco_dragon.dragon_basic import basic as dragon, ddos

keywords = sdecb.keywords
remarks = sdecb.remarks
isdragon = False


def usage(fh, localusage):
    fh.write(
        f'Usage: {sys.argv[0]} [<opts>] [<iname>] [<oname>]\n'
        '\t-b\t--basic=<dialect>\tbasic dialect\n'
        '\t-h\t--help\t\t\tthis help\n'
        '\t-i<n>\t--input=<file>\t\tinput file\n'
        '\t-o<n>\t--output=<file>\t\toutput file\n' + localusage)


def options(args, sopts, lopts, localusage, ext):
    # parse options for coco_dragon utils including globally available options
    global keywords
    global remarks
    global isdragon

    short = "b:hi:o:" + sopts
    long = ["basic=", "help", "input=", "output="] + lopts
    dialects = {
        "cb": (cb.keywords, cb.remarks, False),
        "ecb": (ecb.keywords, ecb.remarks, False),
        "decb": (decb.keywords, decb.remarks, False),
        "secb": (secb.keywords, secb.remarks, False),
        "sdecb": (sdecb.keywords, sdecb.remarks, False),
        "dragon_basic": (dragon.keywords, dragon.remarks, False),
        "ddos": (ddos.keywords, ddos.remarks, False),
    }
    try:
        opts, args = getopt.getopt(args, short, long)
    except getopt.GetoptError as err:
        print(err)
        usage(sys.stderr, localusage)
        sys.exit(2)

    unused = []
    iname = None
    oname = None

    for o, a in opts:
        if o in ["-h", "--help:"]:
            usage(sys.stdout, localusage)
            sys.exit(0)
        elif o in ["-i", "--input"]:
            iname = a
        elif o in ["-o", "--output"]:
            oname = a
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
        else:
            unused.append((o, a))

    if iname is None:
        if len(args) == 0:
            usage(sys.stderr, localusage)
            sys.exit(2)
        iname = args[0]
        args = args[1:]

    if oname is None:
        if len(args) == 0:
            oname = f'{iname}.{ext}'
        else:
            oname = args[0]
            args = args[1:]

    if len(args) != 0:
        usage(sys.stderr, '')
        sys.exit(2)

    return iname, oname, unused
