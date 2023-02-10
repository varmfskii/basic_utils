from msbasic.tokens import Token


class LineNumberError(RuntimeError):
    pass


def getlabs(data):
    # get a list of valid labels (line numbers)
    labels = []

    for line in data:
        if line[0][0] == Token.LABEL:
            labels.append(line[0][1].upper())

    return labels


def gettgtlabs(data):
    # get a list of labels (line numbers) used as targets
    labels = []

    for ix, line in enumerate(data):
        for token in line[1:]:
            if token[0] == Token.LABEL:
                labels.append(token[1].upper())

    labels.sort()
    return labels


def validatelabs(data):
    # check that all labels used as targets are defined
    labs = getlabs(data)
    tgtlabs = gettgtlabs(data)
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


def renumber(data, start=10, interval=10):
    # renumber a parsed BASIC program
    labels = {}
    number = start

    if not validatelabs(data):
        raise LineNumberError('unmatched label') from None

    for ix, line in enumerate(data):
        if line[0][0] == Token.LABEL:
            labels[line[0][1].upper()] = f'{number}'
            data[ix][0] = (Token.LABEL, f'{number}')
        elif line[0][0] == Token.WS:
            data[ix][0] = [(Token.LABEL, f'{number}')]
        else:
            data[ix] = [(Token.LABEL, f'{number}')] + data[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(data):
        for tix, token in enumerate(line):
            if tix == 0:
                continue
            if token[0] == Token.LABEL:
                data[lix][tix] = (Token.LABEL, labels[token[1].upper()])

    return data


def clean_labs(data):
    # remove all line numbers that are not used as targets
    labels = gettgtlabs(data)
    lines = []

    for line in data:
        if not line:
            continue
        if line[0][0] != Token.LABEL or (line[0][0] == Token.LABEL and line[0][1].upper() in labels):
            lines.append(line)
        elif len(line) > 1:
            lines.append(line[1:])

    return lines


def clean_goto(data: list[list[tuple]]) -> list[list[tuple]]:
    # convert "then goto" to "then" and "else goto" to "else"
    rv = []
    for line in data:
        new_line = []
        skip = False
        ll = len(line)
        for ix, token in enumerate(line):
            if skip:
                skip = False
            elif (1 < ix < ll - 1
                  and token[0] == Token.KW and token[1].upper() == 'GO'
                  and line[ix + 1][0] == Token.KW and line[ix + 1][1].upper() == 'TO'
                  and line[ix - 1][0] == Token.KW and line[ix - 1][1].upper() in ['THEN', 'ELSE']):
                skip = True
            else:
                new_line.append(token)
        rv.append(new_line)
    return rv
