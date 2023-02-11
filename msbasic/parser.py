#!/usr/bin/env python3
import re

from msbasic.tokens import Token


class Parser:
    rem_kw = ["'", 'REM']
    data_kw = ['DATA']
    branch_kw = ['GO', 'THEN', 'ELSE']
    ign_kw = ['SUB', 'TO']

    code2kw = {}
    kw2code = {}
    kw_keys = []
    full_parse = None

    def __init__(self, opts, data=None, be=True):
        self.be = be
        for (w, c) in opts.keywords:
            self.code2kw[c] = w
            self.kw2code[w] = c
        self.kw_keys = list(self.kw2code.keys())
        self.kw_keys.sort(key=(lambda x: -len(x)))
        if data:
            self.parse(data)

    def parse(self, data: list[int]) -> list[list[tuple]]:
        if data[0] < 128 and data[1] < 128:
            self.full_parse = self.parse_txt("".join(map(chr, data)))
        else:
            self.full_parse = self.parse_bin(data)
        return self.full_parse

    def parse_bin(self, data: list[int]) -> list[list[tuple]]:
        parsed = []
        while data[0] != 0 or data[1] != 0:
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
                if line[-1][0] == Token.KW and line[-1][1].upper() in self.rem_kw:
                    rem = ''
                    while data[0] != 0:
                        rem += chr(data[0])
                        data = data[1:]
                    if rem != '':
                        line.append((Token.REM, rem))
                elif line[-1][0] == Token.KW and line[-1][1].upper() in self.data_kw:
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
                    identifier = ''
                    while '0' <= chr(c1) <= '9' or 'A' <= chr(c1) <= 'Z' or 'a' <= chr(c1) <= 'z':
                        identifier += chr(data[0])
                        data = data[1:]
                        c1 = data[0]
                    line.append((Token.ID, identifier))
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

    def pass2(self, line: list[tuple]) -> list[tuple]:
        tokens = []
        for token in line:
            if token[0] == Token.NONE:
                tokens += self.split_none(token[1])
            else:
                tokens.append(token)

        nows = self.no_ws(tokens)
        label = 0
        for ix, token in enumerate(nows):
            if label and (token[0] == Token.NUM or (label == 2 and token[0] in [Token.ID, Token.NUM])):
                nows[ix] = (Token.LABEL, token[1])
            elif label and ((token[0] == Token.KW and token[1].upper() not in self.ign_kw) or token[0] == ord(':')):
                label = 0
            if token[0] == Token.ID:
                if ix + 2 < len(nows) and nows[ix + 1][0] == ord('$') and nows[ix + 2][0] == ord('('):
                    nows[ix] = (Token.STRARR, token[1])
                elif ix + 1 < len(nows) and nows[ix + 1][0] == ord('$'):
                    nows[ix] = (Token.STR, token[1])
                elif ix + 1 < len(nows) and nows[ix + 1][0] == ord('('):
                    nows[ix] = (Token.ARR, token[1])
                else:
                    pass
            elif token[0] == Token.KW and token[1].upper() == 'GO':
                label = 2
            elif token[0] == Token.KW and token[1].upper() in self.branch_kw:
                label = 1
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

    @staticmethod
    def split_none(word: str) -> list[tuple]:
        tokens = []
        while word != '':
            match = re.match('[0-9]*\\.[0-9]*', word)
            if match and match.end() > 0:
                ml = match.end()
                tokens.append((Token.FLOAT, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('[0-9]*(\\.[0-9]*)?[+-]?[Ee][0-9]*', word)
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

    @staticmethod
    def no_ws(tokens: list[tuple]) -> list[tuple]:
        rv = []
        for token in tokens:
            if token[0] != Token.WS:
                rv.append(token)
        return rv

    def parse_txt(self, data: str) -> list[list[tuple]]:
        parsed = []
        re.sub('\\\\(\n|\r|\r\n|\n\r)', data, '')
        for linein in re.split('[\n\r]+', data):
            if linein == "":
                continue
            match1 = re.match(' *[0-9]+ *', linein)
            match2 = re.match(' *([A-Za-z][0-9A-Za-z]*): *', linein)
            if match1:
                line = [(Token.LABEL, str(int(linein[:match1.end()])))]
                linein = linein[match1.end():]
            elif match2:
                line = [(Token.LABEL, match2.group(1))]
                linein = linein[match2.end():]
            else:
                line = []
            match = re.match(' *', linein)
            linein = linein[match.end():]
            while linein != '':
                if len(line) > 0:
                    if line[-1][0] == Token.KW and line[-1][1].upper() in self.rem_kw:
                        line.append((Token.REM, linein))
                        linein = ''
                        continue
                    if line[-1][0] == Token.KW and line[-1][1].upper() == 'DATA':
                        match = re.match('[^:]+', linein)
                        if match:
                            ml = match.end()
                            line.append((Token.DATA, linein[:ml]))
                            linein = linein[ml:]
                        continue

                kw = self.match_kw(linein)
                if kw:
                    line.append(kw)
                    linein = linein[len(kw[1]):]
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

    def match_kw(self, line) -> tuple or None:
        ll = len(line)
        for kw in self.kw_keys:
            kl = len(kw)
            if ll >= kl and kw == line[:kl].upper():
                return Token.KW, line[:kl], self.kw2code[kw]
        return None

    def deparse(self, data=None, ws=False) -> str:
        out = ''
        if not data:
            data = self.full_parse
        for line in data:
            out += self.deparse_line(line, ws)
        return out

    def deparse_line(self, line, ws=False):
        if line[0][0] == Token.LABEL:
            out = line[0][1] + ' '
            line = line[1:]
        else:
            out = ' '
        for ix, token in enumerate(line):
            if (token[0] == Token.KW and token[1][0].isalpha() and ix > 0
                and line[ix - 1][0] in [Token.ID, Token.STR, Token.ARR, Token.STRARR]):
                out += ' '
            if ws and out[-1].isalnum() and token[1][0].isalnum():
                out += ' '
            if token[0] in [Token.QUOTED, Token.DATA, Token.REM]:
                out += token[1]
            else:
                out += token[1].upper()
        out += '\n'
        return out;
