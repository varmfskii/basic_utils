import parser
from coco_sdecb import keywords, remarks


class LineNumberError(RuntimeError):
    pass


def tokenize_line(line):
    tokens = []
    for token in line:
        if token[0] == parser.LABEL:  # line number
            val = int(token[1])
            tokens += [val // 256, val & 0xff]
        elif token[0] > 255:  # tokenized extended keyword
            val = token[0]
            tokens += [val // 256, val & 0xff]
        elif token[0] > 127:  # tokenized keyword
            tokens.append(token[0])
        elif token[0] == parser.QUOTED or token[0] == parser.OTHER:  # explicit text
            for char in token[1]:
                tokens.append(ord(char))
        else:
            for char in token[1].upper():  # code text, interpreter only recognizes uppercase
                tokens.append(ord(char))
    tokens.append(0)
    return tokens


def tokenize(data, ws=False, disk=True):
    pp = parser.Parser(keywords, remarks, data)
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    address = 0x2601
    for line in parsed:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 256, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if disk:
        val = len(tokenized)
        tokenized = [255, val // 256, val & 0xff] + tokenized
    return bytearray(tokenized)


def renumber(pp, start=10, interval=10):
    parsed = pp.full_parse
    labels = {}
    number = start

    for ix, line in enumerate(parsed):
        if line[0][0] == parser.LABEL:
            labels[line[0][1]] = f'{number}'
            parsed[ix][0] = (parser.LABEL, f'{number}')
        else:
            parsed[ix] = [(parser.LABEL, f'{number}')] + parsed[ix]
        number += interval
        if number > 32767:
            raise LineNumberError(number) from None

    for lix, line in enumerate(parsed):
        code = parser.NONE
        for tix, token in enumerate(line):
            if token[0] == parser.SEP or (code == pp.kw2code["THEN"] and token[0] not in [parser.NUM, parser.WS]):
                code = parser.NONE
            elif code != parser.NONE and token[0] == parser.NUM:
                parsed[lix][tix] = (parser.NUM, labels[token[1]])
            elif token[0] in [pp.kw2code["THEN"], pp.kw2code["GO"]]:
                code = token[0]

    pp.full_parse = parsed


def getidtype(ix, line):
    if ix + 1 < len(line) and line[ix + 1][1][0] == '$':
        if ix + 2 < len(line) and line[ix + 2][1][0] == '(':
            return 'strarr'
        return 'strvar'
    if ix + 1 < len(line) and line[ix + 1][1][0] == '(':
        return 'numarr'
    return 'numvar'


def getids(pp):
    lines = pp.no_ws()
    numvar = {}
    strvar = {}
    numarr = {}
    strarr = {}

    for line in lines:
        for ix, field in enumerate(line):
            if field[0] == parser.ID:
                var = field[1].upper()
                idtype = getidtype(ix, line)
                # print(var, idtype)
                if idtype == 'strarr':
                    strarr[var] = True
                elif idtype == 'strvar':
                    strvar[var] = True
                elif idtype == 'numarr':
                    numarr[var] = True
                else:
                    numvar[var] = True
    print(numvar)
    print(strvar)
    print(numarr)
    print(strarr)
    return {'numvar': set(numvar.keys()), 'strvar': set(strvar.keys()), 'numarr': set(numarr.keys()),
            'strarr': set(strarr.keys())}
