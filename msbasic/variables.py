from msbasic.parser import Parser
from msbasic.tokens import TokenType, Token


class IDError(RuntimeError):
    pass


def getids(data: [[Token]]) -> dict[TokenType: set]:
    # get a list of all variables used in a program
    numvar = set()
    strvar = set()
    numarr = set()
    strarr = set()

    for line in data:
        for ix, token in enumerate(line):
            if token.isstrarr():
                strarr.add(token.r)
            elif token.isstrvar():
                strvar.add(token.r)
            elif token.isnumarr():
                numarr.add(token.r)
            elif token.isnumvar():
                numvar.add(token.r)
            else:
                pass

    return {TokenType.NUMVAR: numvar, TokenType.STRVAR: strvar, TokenType.NUMARR: numarr,
            TokenType.STRARR: strarr}


def nextid(prev: str) -> str:
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


def getidmap(oldids: [str], pp: Parser) -> dict[str: str]:
    # create a dictionary mapping old variable names to ordinalized variable names
    newids = {}
    newid = ''
    for oldid in oldids:
        newid = nextid(newid)
        while newid in pp.kw2code.keys():
            newid = nextid(newid)
        newids[oldid] = newid
    return newids


def reid(pp: Parser, data: [[Token]] = None) -> [[Token]]:
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
            if token.isvar():
                data[lix][tix].r = mymap[token.t][token.v]
                data[lix][tix].v = mymap[token.t][token.v]

    return data
