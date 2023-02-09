class LineNumberError(RuntimeError):
    pass


def getlabs(pp):
    # get a list of valid labels (line numbers)
    labels = []

    for line in pp.full_parse:
        if line[0][0] == pp.LABEL:
            labels.append(line[0][1])

    return labels


def gettgtlabs(pp):
    # get a list of labels (line numbers) used as targets
    parsed = pp.full_parse
    labels = []

    for line in parsed:
        code = pp.NONE
        for token in line:
            if token[0] == pp.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [pp.NUM, pp.WS]):
                code = pp.NONE
            elif code != pp.NONE and token[0] == pp.NUM and token[1] not in labels:
                labels.append(token[1])
            elif token[0] in [pp.kw2code["THEN"], pp.kw2code["ELSE"], pp.kw2code["GO"]]:
                code = token[0]
    labels.sort()
    return labels


def validatelabs(pp):
    # check that all labels used as targets are defined
    labs = getlabs(pp)
    tgtlabs = gettgtlabs(pp)
    badlabs = []

    for lab in tgtlabs:
        if lab not in labs:
            badlabs.append(lab)

    if len(badlabs) == 0:
        return True
    if len(badlabs) == 1:
        print(f'Bad label: {badlabs[0]}')
    else:
        print(f'Bad labels: {", ".join(badlabs)}')
    return False


def renumber(pp, start=10, interval=10):
    # renumber a parsed BASIC program
    parsed = pp.full_parse
    labels = {}
    number = start

    if not validatelabs(pp):
        raise LineNumberError('unmatched label') from None

    for ix, line in enumerate(parsed):
        if line[0][0] == pp.LABEL:
            labels[line[0][1]] = f'{number}'
            parsed[ix][0] = (pp.LABEL, f'{number}')
        elif line[0][0] == pp.WS:
            parsed[ix] = [(pp.LABEL, f'{number}')] + parsed[ix][1:]
        else:
            parsed[ix] = [(pp.LABEL, f'{number}')] + parsed[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(parsed):
        code = pp.NONE
        for tix, token in enumerate(line):
            if token[0] == pp.SEP or (
                    code in [pp.kw2code["THEN"], pp.kw2code["ELSE"]] and token[0] not in [pp.NUM, pp.WS]):
                code = pp.NONE
            elif code != pp.NONE and token[0] == pp.NUM:
                parsed[lix][tix] = (pp.NUM, labels[token[1]])
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
        if line[0][0] != pp.LABEL or (line[0][0] == pp.LABEL and line[0][1] in labels):
            lines.append(line)
        elif len(line) > 1:
            lines.append(line[1:])

    pp.full_parse = lines
