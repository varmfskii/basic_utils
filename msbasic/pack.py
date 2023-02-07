from msbasic.labels import gettgtlabs, cleanlabs, renumber
from msbasic.variables import reid
from basic69 import Parser


def noremarks(pp):
    # remove all "unnecessary" remarks
    labels = gettgtlabs(pp)
    lines = []

    for line in pp.full_parse:
        for tix, token in enumerate(line):
            if token[0] in [pp.kw2code["REM"], pp.kw2code["'"]]:
                if tix > 0 and line[tix - 1][0] == pp.SEP:
                    line = line[:tix - 1]
                if tix == 0:
                    line = []
                else:
                    line = line[:tix + 1]
                break
        if len(line) == 1 and line[0][0] != pp.LABEL and line[0][1] in labels:
            line += (pp.kw2code["'"], "'")
        if len(line) != 0:
            lines.append(line)

    pp.full_parse = lines


def mergelines(pp, maxlen=0):
    # merge lines in program together where possible to a limit of
    # maxlen (if maxlen is not 0)
    lines = []
    nextline = []
    old_len = 0

    for line in pp.full_parse:
        next_len = linelen(line)
        if line[0][0] == pp.LABEL or 0 < maxlen < old_len + 1 + next_len:
            if nextline:
                lines.append(nextline)
            nextline = line
            old_len = 5 + next_len
        else:
            if nextline:
                nextline += [(pp.SEP, ":")] + line
                old_len += 1 + next_len
            else:
                nextline = line
                old_len = 5 + next_len
        for token in line:
            if token[0] in [pp.kw2code["REM"], pp.kw2code["'"], pp.kw2code["IF"]]:
                lines.append(nextline)
                nextline = []
                break

    if nextline:
        lines.append(nextline)
    pp.full_parse = lines


def splitlines(pp):
    lines = []
    for line in pp.full_parse:
        start = 0
        for ix, field in enumerate(line):
            if field[0] in [pp.kw2code["REM"], pp.kw2code["'"], pp.kw2code["IF"]]:
                break
            if field[0] == pp.SEP:
                lines.append(line[start:ix])
                start = ix + 1
        lines.append(line[start:])
    pp.full_parse = lines


def linelen(line):
    if len(line) == 0:
        return 0
    if line[0][0] == Parser.LABEL:
        line = line[1:]
    len_acc = 0
    for (c, w) in line:
        if 0x80 <= c < 0x100:
            len_acc += 1
        elif c < 0x200:
            len_acc += len(w)
        elif c < 0x10000:
            len_acc += 2
        else:
            len_acc += 3

    return len_acc


def pack(pp, maxline=0):
    # pack a basic program
    pp.full_parse = pp.no_ws()
    reid(pp)
    cleanlabs(pp)
    noremarks(pp)
    mergelines(pp, maxline)
    renumber(pp, start=0, interval=1)
