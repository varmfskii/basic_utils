import parser
from coco.labels import gettgtlabs, cleanlabs, renumber
from coco.variables import reid


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


def pack(pp):
    # pack a basic program
    pp.full_parse = pp.no_ws()
    reid(pp)
    cleanlabs(pp)
    noremarks(pp)
    mergelines(pp)
    renumber(pp, start=0, interval=1)