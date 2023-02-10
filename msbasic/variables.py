from msbasic.tokens import no_ws, Token


class IDError(RuntimeError):
    pass


def getidtype(ix, line, pp):
    # decide what kind of variable is pointed to by ix in line
    if line[ix][0] != pp.ID:
        return None
    if ix + 1 < len(line) and line[ix + 1][1][0] == '$':
        if ix + 2 < len(line) and line[ix + 2][1][0] == '(':
            return 'strarr'
        return 'strvar'
    if ix + 1 < len(line) and line[ix + 1][1][0] == '(':
        return 'numarr'
    return 'numvar'


def getids(data: list[list[tuple]]) -> dict[Token, set]:
    # get a list of all variables used in a program
    lines = no_ws(data)
    numvar = set()
    strvar = set()
    numarr = set()
    strarr = set()

    for line in lines:
        for ix, token in enumerate(line):
            if token[0] == Token.STRARR:
                strarr.add(token[1].upper())
            elif token[0] == Token.STR:
                strvar.add(token[1].upper())
            elif token[0] == Token.ARR:
                numarr.add(token[1].upper())
            elif token[0] == Token.ID:
                numvar.add(token[1].upper())
            else:
                pass

    return {Token.ID: numvar, Token.STR: strvar, Token.ARR: numarr,
            Token.STRARR: strarr}


def nextid(prev):
    # get the next available variable name
    if len(prev) == 0:
        return 'A'
    if len(prev) == 1:
        if prev == 'L':
            return 'N'
        if prev == 'Z':
            return 'A0'
        return chr(ord(prev) + 1)
    if prev == 'ZZ':
        raise IDError
    if prev[1] == '9':
        return prev[0] + 'A'
    if prev[1] == 'Z':
        if prev[0] == 'L':
            return 'N0'
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


def reid(pp, data=None) -> list[list[tuple]]:
    # remap variable names in a program to ordialized variable names
    if not data:
        data = pp.full_parse
    oldids = getids(data)
    mymap = {}
    for key in oldids.keys():
        ids = oldids[key]
        mymap[key] = getidmap(ids, pp)

    for lix, line in enumerate(data):
        for tix, token in enumerate(line):
            if token[0] in [Token.ID, Token.STR, Token.ARR, Token.STRARR]:
                data[lix][tix] = (token[0], mymap[token[0]][token[1].upper()])

    return data
