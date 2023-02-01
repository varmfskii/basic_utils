from coco_dragon.labels import gettgtlabs, cleanlabs, renumber
from coco_dragon.variables import reid


def noremarks(pp):
    # remove all "unnecessary" remarks
    labels = gettgtlabs(pp)
    lines = []

    for line in pp.full_parse:
        for tix, token in enumerate(line):
            if token[0] in [pp.kw2code["REM"], pp.kw2code["'"]]:
                if tix > 0 and line[tix - 1][0] == pp.SEP:
                    line = line[:tix-1]
                if tix == 0:
                    line = []
                else:
                    line = line[:tix+1]
                break
        if len(line) == 1 and line[0][0] != pp.LABEL and line[0][1] in labels:
            line += (pp.kw2code["'"], "'")
        if len(line) != 0:
            lines.append(line)

    pp.full_parse = lines


def mergelines(pp):
    # merge lines in program together where possible
    lines = []
    nextline = []

    for line in pp.full_parse:
        if line[0][0] == pp.LABEL:
            if nextline:
                lines.append(nextline)
            nextline = line
        else:
            if nextline:
                nextline += [(pp.SEP, ":")] + line
            else:
                nextline = line
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
                start = ix+1
        lines.append(line[start:])
    pp.full_parse = lines


def pack(pp):
    # pack a basic program
    pp.full_parse = pp.no_ws()
    reid(pp)
    cleanlabs(pp)
    noremarks(pp)
    mergelines(pp)
    renumber(pp, start=0, interval=1)
