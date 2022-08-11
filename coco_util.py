import getopt
import random
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


class IDError(RuntimeError):
    pass


def options(args, sopts, lopts, usage, ext):
    # parse options for coco utils including globally available options
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
    # get a list of valid labels (line numbers)
    labels = []

    for line in pp.full_parse:
        if line[0][0] == parser.LABEL:
            labels.append(line[0][1])

    return labels


def gettgtlabs(pp):
    # get a list of labels (line numbers) used as targets
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
    # check that all labels used as targets are defined
    labs = getlabs(pp)
    tgtlabs = gettgtlabs(pp)

    for lab in tgtlabs:
        if lab not in labs:
            return False

    return True


def tokenize_line(line):
    # convert a parsed line into the tokenized format for a BASIC file
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


def tokenize(pp, ws=False, disk=True):
    # convert a parsed file into tokenized BASIC file
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    if disk:
        address = 0x2601
    else:
        address = 0x25fe
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
    # renumber a parsed BASIC program
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
            elif token[0] in [pp.kw2code["THEN"], pp.kw2code["ELSE"], pp.kw2code["GO"]]:
                code = token[0]

    pp.full_parse = parsed


def getidtype(ix, line):
    # decide what kind of variable is pointed to by ix in line
    if line[ix][0] != parser.ID:
        return None
    if ix + 1 < len(line) and line[ix + 1][1][0] == '$':
        if ix + 2 < len(line) and line[ix + 2][1][0] == '(':
            return 'strarr'
        return 'strvar'
    if ix + 1 < len(line) and line[ix + 1][1][0] == '(':
        return 'numarr'
    return 'numvar'


def getids(pp):
    # get a list of all variables used in a program
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
    # remove all line numbers that are not used as targets
    labels = gettgtlabs(pp)
    parsed = pp.full_parse
    lines = []

    for line in parsed:
        if not line:
            continue
        if line[0][0] != parser.LABEL or (line[0][0] == parser.LABEL and line[0][1] in labels):
            lines.append(line)
        elif len(line) > 1:
            lines.append(line[1:])

    pp.full_parse = lines


def noremarks(pp):
    # remove all "unnecessary" remarks
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


def mergelines(pp):
    # merge lines in program together where possible
    lines = []
    nextline = []

    for line in pp.full_parse:
        if not nextline:
            nextline = line
        elif line[0][0] == parser.LABEL:
            lines.append(nextline)
            nextline = line
        else:
            nextline += [(parser.SEP, ":")] + line
            last = False
            for token in line:
                if token[0] in [pp.kw2code["REM"], pp.kw2code["'"], pp.kw2code["IF"]]:
                    last = True
                    break
            if last:
                lines.append(nextline)
                nextline = []
    if nextline:
        lines.append(nextline)
    pp.full_parse = lines


def nextid(prev):
    # get the next available variable name
    if len(prev) == 0:
        return 'A'
    if len(prev) == 1:
        if prev == 'Z':
            return 'A0'
        return chr(ord(prev) + 1)
    if prev == 'ZZ':
        raise IDError
    if prev[1] == '9':
        return prev[0] + 'A'
    if prev[1] == 'Z':
        return chr(ord(prev[0]) + 1) + '0'
    return prev[0] + chr(ord(prev[1]) + 1)


def getidmap(oldids, pp):
    # create a dictionary mapping old variable names to ordinalized variable names
    newids = {}
    newid = ''
    for oldid in oldids:
        newid = nextid(newid)
        while newid in pp.kw2code.keys():
            newid = nextid(newid)
        newids[oldid] = newid
    return newids


def reid(pp):
    # remap variable names in a program to ordialized variable names
    oldids = getids(pp)
    mymap = {}
    for key in oldids.keys():
        ids = oldids[key]
        mymap[key] = getidmap(ids, pp)

    data = pp.no_ws()

    for lix, line in enumerate(data):
        for tix, token in enumerate(line):
            if token[0] == parser.ID:
                data[lix][tix] = (parser.ID, mymap[getidtype(tix, line)][token[1].upper()])

    pp.full_parse = data


def pack(pp):
    # pack a basic program
    pp.full_parse = pp.no_ws()
    reid(pp)
    cleanlabs(pp)
    noremarks(pp)
    mergelines(pp)
    renumber(pp, start=0, interval=1)
