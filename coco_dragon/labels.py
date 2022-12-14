from parser import Types

class LineNumberError(RuntimeError):
    pass


def getlabs(pp):
    # get a list of valid labels (line numbers)
    labels = []

    for line in pp.full_parse:
        if line[0][0] == Types.LABEL:
            labels.append(line[0][1])

    return labels


def gettgtlabs(pp):
    # get a list of labels (line numbers) used as targets
    parsed = pp.full_parse
    labels = []

    for line in parsed:
        code = Types.NONE
        for token in line:
            if token[0] == Types.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [Types.NUM, Types.WS]):
                code = Types.NONE
            elif code != Types.NONE and token[0] == Types.NUM and token[1] not in labels:
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


def renumber(pp, start=10, interval=10):
    # renumber a parsed BASIC program
    parsed = pp.full_parse
    labels = {}
    number = start

    if not validatelabs(pp):
        raise LineNumberError('unmatched label') from None

    for ix, line in enumerate(parsed):
        if line[0][0] == Types.LABEL:
            labels[line[0][1]] = f'{number}'
            parsed[ix][0] = (Types.LABEL, f'{number}')
        elif line[0][0] == Types.WS:
            parsed[ix] = [(Types.LABEL, f'{number}')] + parsed[ix][1:]
        else:
            parsed[ix] = [(Types.LABEL, f'{number}')] + parsed[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(parsed):
        code = Types.NONE
        for tix, token in enumerate(line):
            if token[0] == Types.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [Types.NUM, Types.WS]):
                code = Types.NONE
            elif code != Types.NONE and token[0] == Types.NUM:
                parsed[lix][tix] = (Types.NUM, labels[token[1]])
            elif token[0] in [pp.kw2code["THEN"], pp.kw2code["ELSE"], pp.kw2code["GO"]]:
                code = token[0]

    pp.full_parse = parsed


def cleanlabs(pp):
    # remove all line numbers that are not used as targets
    labels = gettgtlabs(pp)
    parsed = pp.full_parse
    lines = []

    for line in parsed:
        if not line:
            continue
        if line[0][0] != Types.LABEL or (line[0][0] == Types.LABEL and line[0][1] in labels):
            lines.append(line)
        elif len(line) > 1:
            lines.append(line[1:])

    pp.full_parse = lines
