#!/usr/bin/env python3
import re
import sys
from enum import Enum

from basic69.coco import sdecb


class Token(Enum):
    NONE = 256
    LABEL = 257
    TOKEN = 258
    ID = 259
    STR = 260
    ARR = 261
    STRARR = 262
    QUOTED = 263
    REM = 264
    DATA = 265
    NUM = 266
    HEX = 267
    FLOAT = 268
    WS = 269
    KW = 270

    def __repr__(self):
        return self.name


class Parser:
    code2kw = {}
    kw2code = {}
    full_parse = None
    rem_codes = []

    def __init__(self, keywords, remarks, data=None, be=True):
        self.be = be
        for (w, c) in keywords:
            self.code2kw[c] = w
            self.kw2code[w] = c
        if data:
            self.parse(data)
        for rem in remarks:
            self.rem_codes.append(self.kw2code[rem])

    def parse(self, data):
        if data[0] == 0xff:
            self.full_parse = self.parse_bin(data[3:])
        elif data[0] == 0x55 and data[1] == 0:
            self.full_parse = self.parse_bin(data[9:])
        elif data[0] < 128 and data[1] < 128:
            self.full_parse = self.parse_txt("".join(map(chr, data)))
        else:
            self.full_parse = self.parse_bin(data)
        return self.full_parse

    def parse_bin(self, data):
        parsed = []
        while (data[0] != 0 or data[1] != 0):
            data = data[2:]
            if self.be:
                line = [(Token.LABEL, str(data[0] * 0x100 + data[1]))]
            else:
                line = [(Token.LABEL, str(data[0] + data[1] * 0x100))]
            data = data[2:]
            while data[0] != 0:
                c1 = data[0]
                if len(data) > 1:
                    c2 = c1 * 0x100 + data[1]
                else:
                    c2 = c1 * 0x100
                if len(data) > 2:
                    c3 = c2 * 0x100 + data[2]
                else:
                    c3 = c2 * 0x100
                if line[-1][0] == Token.KW and line[-1][1].upper() in ["'", "REM"]:
                    rem = ''
                    while data[0] != 0:
                        rem += chr(data[0])
                        data = data[1:]
                    if rem != '':
                        line.append((Token.REM, rem))
                elif line[-1][0] == Token.KW and line[-1][2] == self.kw2code['DATA']:
                    data_data = ''
                    while data[0] != 0 and data[0] != ord(':'):
                        data_data += chr(data[0])
                        data = data[1:]
                    if data != '':
                        line.append((Token.DATA, data_data))
                elif c3 in self.code2kw.keys():
                    # 3-byte token
                    data = data[3:]
                    line.append((Token.KW, self.code2kw[c3], c3))
                elif c2 in self.code2kw.keys():
                    # 2-byte token
                    data = data[2:]
                    line.append((Token.KW, self.code2kw[c2], c2))
                elif c1 in self.code2kw.keys():
                    # 1-byte token
                    data = data[1:]
                    line.append((Token.KW, self.code2kw[c1], c1))
                elif 'A' <= chr(c1) <= 'Z' or 'a' <= chr(c1) <= 'z':
                    # id
                    id = ''
                    while '0' <= chr(c1) <= '9' or 'A' <= chr(c1) <= 'Z' or 'a' <= chr(c1) <= 'z':
                        id += chr(data[0])
                        data = data[1:]
                        c1 = data[0]
                    line.append((Token.ID, id))
                elif c1 == ord('"'):
                    # quoted
                    quote = '"'
                    data = data[1:]
                    while data[0] != 0 and data[0] != ord('"'):
                        quote += chr(data[0])
                        data = data[1:]
                    if data[0] != 0:
                        quote += '"'
                        data = data[1:]
                        line.append((Token.QUOTED, quote))
                elif line[-1][0] == Token.NONE:
                    data = data[1:]
                    line[-1] = (Token.NONE, line[-1][1] + chr(c1))
                else:
                    data = data[1:]
                    line.append((Token.NONE, chr(c1)))
            data = data[1:]
            parsed.append(self.pass2(line))
        return parsed

    def pass2(self, line):
        tokens = []
        for token in line:
            if token[0] == Token.NONE:
                tokens += self.split_none(token[1])
            else:
                tokens.append(token)

        nows = self.nows(tokens)
        nl = len(nows)
        label = False
        for ix, token in enumerate(nows):
            if label:
                if token[0] in [Token.ID, Token.NUM]:
                    nows[ix] = (Token.LABEL, token[1])
                elif (token[0] == Token.KW and token[1] not in ['TO', 'SUB']) or token[0] == ord(':'):
                    label = False
                else:
                    pass
            else:
                if token[0] == Token.ID:
                    if ix + 2 < len(nows) and nows[ix + 1][0] == ord('$') and nows[ix + 2][0] == ord('('):
                        nows[ix] = (Token.STRARR, token[1])
                    elif ix + 1 < len(nows) and nows[ix + 1][0] == ord('$'):
                        nows[ix] = (Token.STR, token[1])
                    elif ix + 1 < len(nows) and nows[ix + 1][0] == ord('('):
                        nows[ix] = (Token.ARR, token[1])
                    else:
                        pass
                elif token[0] == Token.KW and token[1].upper() in ['GO', 'THEN', 'ELSE']:
                    label = True
                else:
                    pass

        i = 0
        j = 0
        while i < len(tokens):
            if tokens[i][0] == Token.WS:
                i += 1
            else:
                tokens[i] = nows[j]
                i += 1
                j += 1

        return tokens

    def split_none(self, word):
        tokens = []
        while word != '':
            match = re.match('[0-9]*\.[0-9]*', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.FLOAT, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('[0-9]*(\.[0-9]*)?[+-]?[Ee][0-9]*', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.FLOAT, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('[0-9]*', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.NUM, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('&H[0-9A-Fa-f]*', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.HEX, word[:ml]))
                word = word[ml:]
                continue
            match = re.match(' *', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.WS, word[:ml]))
                word = word[ml:]
                continue
            tokens.append((ord(word[0]), word[0]))
            word = word[1:]
        return tokens

    def nows(self, tokens):
        rv = []
        for token in tokens:
            if token[0] != Token.WS:
                rv.append(token)
        return rv

    def parse_txt(self, data, be=True):
        parsed = []
        for linein in re.split('[\n\r]+', data):
            if linein == "":
                continue
            match1 = re.match(' *[0-9]+ *', linein)
            match2 = re.match(' *[A-Za-z][0-9A-Za-z]*: *', linein)
            if match1:
                line = [(Token.LABEL, str(int(linein[:match1.end()])))]
                linein = linein[match1.end():]
            elif match2:
                line = [(Token.LABEL, str(int(linein[:match2.end() - 1])))]
                linein = linein[match2.end():]
            else:
                line = []
            match = re.match(' *', linein)
            linein = linein[match.end():]
            while linein != '':
                if len(line) > 0:
                    if line[-1][0] == Token.KW and line[-1][2] in self.rem_codes:
                        line.append((Token.REM, linein))
                        linein = ''
                        continue
                    if line[-1][0] == self.kw2code['DATA']:
                        match = re.match('[^:]+', linein)
                        if match:
                            ml = match.end()
                            line.append((Token.DATA, linein[:ml]))
                            linein = linein[ml:]
                        continue

                found = False
                for kw in self.kw2code.keys():
                    kl = len(kw)
                    if linein[:kl].upper() == kw:
                        found = True
                        line.append((Token.KW, linein[:kl], self.kw2code[kw]))
                        linein = linein[kl:]
                        break
                if found:
                    continue

                match = re.match('[A-Za-z][0-9A-Za-z]*', linein)
                if match:
                    ml = match.end()
                    line.append((Token.ID, linein[:ml]))
                    linein = linein[ml:]
                    continue

                match = re.match('"[^"]*"', linein)
                if match:
                    ml = match.end()
                    line.append((Token.QUOTED, linein[:ml]))
                    linein = linein[ml:]
                    continue

                if line[-1][0] == Token.NONE:
                    line[-1] = (Token.NONE, line[-1][1] + linein[0])
                else:
                    line.append((Token.NONE, linein[0]))
                linein = linein[1:]
            parsed.append(self.pass2(line))
        return parsed


pp = Parser(sdecb.keywords, sdecb.remarks)

for fn in sys.argv[1:]:
    data = open(fn, "rb").read()
    parsed = pp.parse(data)
    for line in parsed:
        print(line)
