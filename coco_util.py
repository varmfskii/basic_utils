import getopt
import sys

import coco_cb as cb
import coco_decb as decb
import coco_ecb as ecb
import coco_sdecb as sdecb
import coco_secb as secb
import parser

keywords = sdecb.keywords
remarks = sdecb.remarks


class LineNumberError(RuntimeError):
    pass


def options(args, sopts, lopts, usage, ext):
    global keywords
    global remarks

    short = "hi:o:" + sopts
    long = ["cb", "ecb", "secb", "decb", "sdecb", "help", "input=", "output="] + lopts
    try:
        opts, args = getopt.getopt(args, short, long)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    unused = []
    iname = None
    oname = None

    for o, a in opts:
        if o in ["-h", "--help:"]:
            usage()
            sys.exit(0)
        elif o in ["-i", "--input"]:
            iname = a
        elif o in ["-o", "--output"]:
            oname = a
        elif o == "--cb":
            keywords = cb.keywords
            remarks = cb.remarks
        elif o == "--ecb":
            keywords = ecb.keywords
            remarks = ecb.remarks
        elif o == "--decb":
            keywords = decb.keywords
            remarks = decb.remarks
        elif o == "--secb":
            keywords = secb.keywords
            remarks = secb.remarks
        elif o == "--sdecb":
            keywords = sdecb.keywords
            remarks = sdecb.remarks
        else:
            unused.append((o, a))

    if iname is None:
        if len(args) == 0:
            usage()
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
        usage()
        sys.exit(2)

    return iname, oname, unused


def getlabs(pp):
    labels = []

    for line in pp.full_parse:
        if line[0][0] == parser.LABEL:
            labels.append(line[0][1])

    return labels


def gettgtlabs(pp):
    parsed = pp.full_parse
    labels = []

    for line in parsed:
        code = parser.NONE
        for token in line:
            if token[0] == parser.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [parser.NUM, parser.WS]):
                code = parser.NONE
            elif code != parser.NONE and token[0] == parser.NUM and token[1] not in labels:
                labels.append(token[1])
            elif token[0] in [pp.kw2code["THEN"], pp.kw2code["ELSE"], pp.kw2code["GO"]]:
                code = token[0]
    labels.sort()
    return labels


def validatelabs(pp):
    labs = getlabs(pp)
    tgtlabs = gettgtlabs(pp)

    for lab in tgtlabs:
        if lab not in labs:
            return False

    return True


def tokenize_line(line):
    tokens = []
    for token in line:
        if token[0] == parser.LABEL:  # line number
            val = int(token[1])
            tokens += [val // 256, val & 0xff]
        elif token[0] > 255:  # tokenized extended keyword
            val = token[0]
            tokens += [val // 256, val & 0xff]
        elif token[0] > 127:  # tokenized keyword
            tokens.append(token[0])
        elif token[0] == parser.QUOTED or token[0] == parser.OTHER:  # explicit text
            for char in token[1]:
                tokens.append(ord(char))
        else:
            for char in token[1].upper():  # code text, interpreter only recognizes uppercase
                tokens.append(ord(char))
    tokens.append(0)
    return tokens


def tokenize(data, ws=False, disk=True):
    pp = parser.Parser(keywords, remarks, data)
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    address = 0x2601
    for line in parsed:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 256, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if disk:
        val = len(tokenized)
        tokenized = [255, val // 256, val & 0xff] + tokenized
    return bytearray(tokenized)


def renumber(pp, start=10, interval=10):
    parsed = pp.full_parse
    labels = {}
    number = start

    if not validatelabs(pp):
        raise LineNumberError('unmatched label') from None

    for ix, line in enumerate(parsed):
        if line[0][0] == parser.LABEL:
            labels[line[0][1]] = f'{number}'
            parsed[ix][0] = (parser.LABEL, f'{number}')
        else:
            parsed[ix] = [(parser.LABEL, f'{number}')] + parsed[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(parsed):
        code = parser.NONE
        for tix, token in enumerate(line):
            if token[0] == parser.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [parser.NUM, parser.WS]):
                code = parser.NONE
            elif code != parser.NONE and token[0] == parser.NUM:
                parsed[lix][tix] = (parser.NUM, labels[token[1]])
            elif token[0] in [pp.kw2code["THEN"], pp.kwcode["ELSE"], pp.kw2code["GO"]]:
                code = token[0]

    pp.full_parse = parsed


def getidtype(ix, line):
    if ix + 1 < len(line) and line[ix + 1][1][0] == '$':
        if ix + 2 < len(line) and line[ix + 2][1][0] == '(':
            return 'strarr'
        return 'strvar'
    if ix + 1 < len(line) and line[ix + 1][1][0] == '(':
        return 'numarr'
    return 'numvar'


def getids(pp):
    lines = pp.no_ws()
    numvar = {}
    strvar = {}
    numarr = {}
    strarr = {}

    for line in lines:
        for ix, field in enumerate(line):
            if field[0] == parser.ID:
                var = field[1].upper()
                idtype = getidtype(ix, line)
                if idtype == 'strarr':
                    strarr[var] = True
                elif idtype == 'strvar':
                    strvar[var] = True
                elif idtype == 'numarr':
                    numarr[var] = True
                else:
                    numvar[var] = True

    return {'numvar': set(numvar.keys()), 'strvar': set(strvar.keys()), 'numarr': set(numarr.keys()),
            'strarr': set(strarr.keys())}


def cleanlabs(pp):
    labels = gettgtlabs(pp)
    parsed = pp.full_parse
    lines = []

    for line in parsed:
        if line[0][0] == parser.LABEL and line[0][1] in labels:
            lines.append(line)
        elif len(line) > 1:
            lines.append(line[1:])

    pp.full_parse = lines


def noremarks(pp):
    labels = gettgtlabs(pp)
    lines = []

    for line in pp.full_parse:
        for tix, token in enumerate(line):
            if token[0] in [pp.kw2code["REM"], pp.kw2code["'"]]:
                if tix > 0 and line[tix - 1][0] == parser.SEP:
                    tix -= 1
                if tix == 0:
                    line = []
                else:
                    line = line[tix - 1:]
                break
        if len(line) == 1 and line[0][0] != parser.LABEL and line[0][1] in labels:
            line += (pp.kw2code["'"], "'")
        if len(line) != 0:
            lines.append(line)

    pp.full_parse = lines
