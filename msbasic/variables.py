from parser import Parser


class IDError(RuntimeError):
    pass


def getidtype(ix, line):
    # decide what kind of variable is pointed to by ix in line
    if line[ix][0] != Parser.ID:
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
            if field[0] == Parser.ID:
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
            if token[0] == Parser.ID:
                data[lix][tix] = (Parser.ID, mymap[getidtype(tix, line)][token[1].upper()])

    pp.full_parse = data
