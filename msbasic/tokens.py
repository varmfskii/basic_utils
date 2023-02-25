import re
from enum import Enum

from msbasic.options import Options


class TokenType(Enum):
    NONE = 256
    LABEL = 257
    KW = 258
    NUMVAR = 259
    STRVAR = 260
    NUMARR = 261
    STRARR = 262
    QUOTED = 263
    REM = 264
    DATA = 265
    DEC = 266
    HEX = 267
    FLOAT = 268
    WS = 269

    def __repr__(self):
        return self.name


class Token:
    t: TokenType
    r: str
    v: any

    def __init__(self, t=None, r=None, v=None, m=None):
        self.t = t
        self.r = r
        self.v = v
        self.kw2code = m

    @staticmethod
    def none(v: str):
        return Token(TokenType.NONE, v, re.sub(' ', '', v).upper())

    def none_append(self, v: str):
        self.r += v
        self.v += re.sub(' ', '', v).upper()

    def isnone(self):
        return self.t == TokenType.NONE

    @staticmethod
    def label(v: str):
        return Token(TokenType.LABEL, v, re.sub(' ', '', v).upper())

    def islabel(self):
        return self.t == TokenType.LABEL

    def kw(self, v: str):
        v = v.upper()
        return Token(TokenType.KW, v, self.kw2code[v])

    def iskw(self):
        return self.t == TokenType.KW

    def matchkw(self, v: [str]):
        return self.t == TokenType.KW and self.r in v

    @staticmethod
    def numvar(v: str):
        return Token(TokenType.NUMVAR, v, re.sub(' ', '', v).upper())

    def isnumvar(self):
        return self.t == TokenType.NUMVAR

    @staticmethod
    def strvar(v: str):
        return Token(TokenType.STRVAR, v, re.sub(' ', '', v).upper())

    def isstrvar(self):
        return self.t == TokenType.STRVAR

    @staticmethod
    def numarr(v: str):
        return Token(TokenType.NUMARR, v, re.sub(' ', '', v).upper())

    def isnumarr(self):
        return self.t == TokenType.NUMARR

    @staticmethod
    def strarr(v: str):
        return Token(TokenType.STRARR, v, re.sub(' ', '', v).upper())

    def isstrarr(self):
        return self.t == TokenType.STRARR

    def isvar(self):
        return self.t in [TokenType.NUMARR, TokenType.NUMVAR, TokenType.STRARR, TokenType.STRVAR]

    @staticmethod
    def quoted(v: str):
        return Token(TokenType.QUOTED, v, v[1:-1])

    def isquoted(self):
        return self.t == TokenType.QUOTED

    @staticmethod
    def rem(v: str):
        return Token(TokenType.REM, v, None)

    def isrem(self):
        return self.t == TokenType.REM

    @staticmethod
    def data(v: str):
        return Token.data_list(split_data(v))

    @staticmethod
    def data_list(d: [str]):
        return Token(TokenType.DATA, ','.join(d), d)

    def isdata(self):
        return self.t == TokenType.DATA

    @staticmethod
    def dec(v: str):
        return Token(TokenType.DEC, v, int(v))

    def isdec(self):
        return self.t == TokenType.DEC

    @staticmethod
    def hex(v: str):
        return Token(TokenType.HEX, v, int(v[2:], 16))

    def ishex(self):
        return self.t == TokenType.HEX

    def isint(self):
        return self.t in [TokenType.DEC, TokenType.HEX]

    @staticmethod
    def float(v: str):
        if v == '.':
            return Token(TokenType, '.', 0)
        else:
            return Token(TokenType.FLOAT, v, float(v))

    def isfloat(self):
        return self.t == TokenType.FLOAT

    def isnum(self):
        return self.t in [TokenType.DEC, TokenType.HEX, TokenType.FLOAT]

    @staticmethod
    def ws(v: str):
        return Token(TokenType.WS, v, None)

    @staticmethod
    def other(c: str):
        return Token(ord(c), c, c)

    def __repr__(self):
        return f'({self.t}, {self.r}, {self.v})'


def tokenize(data: [[tuple[int, str] or tuple[int, str, int]]], opts: Options, be=True) -> [int]:
    # convert a parsed file into tokenized BASIC file
    address = opts.address
    tokenized = []
    for line in data:
        line_tokens = tokenize_line(line, be=be)
        address += 2 + len(line_tokens)
        if be:
            tokenized += [address // 0x0100, address & 0xff] + line_tokens
        else:
            tokenized += [address & 0xff, address // 0x0100] + line_tokens
    return tokenized


def tokenize_line(line: [Token], be=True) -> [int]:
    # convert a parsed line into the tokenized format for a BASIC file
    val = int(line[0].r)
    if be:
        tokens = [val // 256, val & 0xff]
    else:
        tokens = [val & 0xff, val // 256]
    for token in line[1:]:
        if not token.iskw():
            for char in token.r:
                tokens.append(ord(char))
        elif token.v < 0x100:  # tokenized keyword
            tokens.append(token.v)
        elif token.v < 0x10000:  # tokenized extended keyword
            tokens += [token.v // 256, token.v & 0xff]
        else:  # three byte keyword
            tokens += [token.v // 0x10000, (token.v // 0x100) & 0xff, token.v & 0xff]
    tokens.append(0)
    return tokens


def detokenize_body(data, pp, be=True):
    listing = ""
    ix = 0

    while data[ix] != 0x00 or data[ix + 1] != 0x00:
        if be:
            line = f'{data[ix + 2] * 0x100 + data[ix + 3]} '
        else:
            line = f'{data[ix + 2] + data[ix + 3] * 0x100} '

        ix += 4
        lastid = False
        while data[ix] != 0x00:
            c1 = data[ix]
            ix = ix + 1
            c2 = data[ix]
            if c1 * 0x100 + c2 in pp.code2kw.keys():
                kw = pp.code2kw[c1 * 0x100 + c2]
                ix += 1
                iskw = True
            elif c1 in pp.code2kw.keys():
                kw = pp.code2kw[c1]
                iskw = True
            else:
                kw = chr(c1)
                iskw = False
                if kw.isalpha():
                    # A-Z
                    lastid = True
                elif not kw.isdigit():
                    # not 0-9
                    lastid = False
            if iskw:
                if lastid and kw[0].isalpha():
                    line += ' '
                lastid = False
            line += kw

        ix += 1
        pp.parse_txt(line)
        listing += line + '\n'

    return pp, listing


def split_data(s: str) -> [str]:
    d = []
    n = ''
    inquote = False
    for c in s:
        if inquote or c != ',':
            n += c
        else:
            while n[0] == ' ':
                n = n[1:]
            while n[-1] == ' ':
                n = n[:-1]
            d.append(n)
            n = ''
        if c == '"':
            inquote = not inquote
    if d or n:
        while n[0] == ' ':
            n = n[1:]
        while n[-1] == ' ':
            n = n[:-1]
        d.append(n)
    return d
