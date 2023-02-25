from msbasic.tokens import Token


class LineNumberError(RuntimeError):
    pass


def getlabs(data: [[Token]]) -> [str]:
    # get a list of valid labels (line numbers)
    labels = []

    for line in data:
        if line[0].islabel():
            labels.append(line[0].v)
    return labels


def gettgtlabs(data: [[Token]]) -> [str]:
    # get a list of labels (line numbers) used as targets
    labels = []

    for ix, line in enumerate(data):
        for token in line[1:]:
            if token.islabel():
                labels.append(token.v)

    labels.sort()
    return labels


def validatelabs(data: [[Token]]) -> bool:
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


def renumber(data: [[Token]], start: int = 10, interval: int = 10) -> [[Token]]:
    # renumber a parsed BASIC program
    labels = {}
    number = start

    if not validatelabs(data):
        raise LineNumberError('unmatched label') from None

    for ix, line in enumerate(data):
        if line[0].islabel():
            labels[line[0].v] = f'{number}'
            data[ix][0] = Token.label(f'{number}')
        else:
            data[ix] = [Token.label(f'{number}')] + data[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(data):
        for tix, token in enumerate(line):
            if tix == 0:
                continue
            if token.islabel():
                data[lix][tix] = Token.label(labels[token.v])
    return data
