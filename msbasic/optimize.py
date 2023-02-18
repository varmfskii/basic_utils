import re
from enum import Flag, auto

from msbasic.labels import gettgtlabs, renumber
from msbasic.tokens import Token, no_ws
from msbasic.variables import reid


class OFlags(Flag):
    I2X = auto()
    Z2P = auto()
    QUOTE = auto()
    TEXTLEN = auto()


class Optimizer:
    def __init__(self, parser, data=None):
        self.pp = parser
        if data:
            self.data = data
        else:
            self.data = parser.full_parse

    def no_remarks(self):
        # remove all "unnecessary" remarks
        lines = []

        for line in self.data:
            for tix, token in enumerate(line):
                if token[1].upper() in self.pp.rem_kw:
                    if tix > 0 and line[tix - 1][0] == ord(':'):
                        line = line[:tix - 1]
                    else:
                        line = line[:tix]
                    break
            if len(line) != 0:
                lines.append(line)

        self.data = lines

    def merge_lines(self, max_len=0, text_len=False):
        # merge lines in program together where possible to a limit of
        # maxlen (if maxlen is not 0)
        lines = []
        nextline = []
        if text_len:
            old_len = 1
        else:
            old_len = 4
        line_no = 0

        if not self.data:
            self.data = self.pp.full_parse
        for line in self.data:
            if not line:
                continue
            next_len = get_len(self.pp, line, text_len=text_len)
            if line[0][0] == Token.LABEL or 0 < max_len < old_len + 1 + next_len:
                if nextline:
                    lines.append(nextline)
                    line_no += 1
                nextline = line
                old_len = next_len
                if text_len:
                    old_len += len(str(line_no)) + 1
                else:
                    old_len += 5
            else:
                if nextline:
                    data_data = ''
                    if nextline[-1][0] == Token.DATA:
                        data_data = nextline[-1][1]
                        nextline = nextline[:-2]
                        if len(nextline) > 0 and nextline[-1] == (ord(':'), ':'):
                            nextline = nextline[:-1]
                    if line[-1][0] == Token.DATA:
                        if data_data:
                            data_data += ','
                        new_data = line[-1][1]
                        new_data = re.sub('^ *', '', new_data)
                        data_data += new_data
                        line = line[:-2]
                        if len(line) > 0 and line[-1] == (ord(':'), ':'):
                            line = line[:-1]
                    if len(nextline) > 0 and len(line) > 0:
                        nextline += [(ord(':'), ':')]
                        old_len += 1
                    nextline += line
                    old_len += next_len
                    if data_data:
                        if len(nextline) > 1 or nextline[0][0] != Token.LABEL:
                            nextline += [(ord(':'), ':')]
                        nextline += [(Token.KW, self.pp.data_kw[0], self.pp.kw2code[self.pp.data_kw[0]]),
                                     (Token.DATA, data_data)]
                else:
                    nextline = line
                    old_len = 5 + next_len
            for token in line:
                if token[0] == Token.KW and token[1].upper() == 'IF':
                    lines.append(nextline)
                    line_no += 1
                    nextline = []
                    if text_len:
                        old_len = len(str(line_no))
                    else:
                        old_len = 4
                    break

        if nextline:
            lines.append(nextline)
        self.data = lines

    def clean_goto(self):
        # convert "then goto" to "then" and "else goto" to "else"
        # remove "let" keyword
        rv = []
        for line in self.data:
            new_line = []
            skip = False
            ll = len(line)
            for ix, token in enumerate(line):
                if skip:
                    skip = False
                elif (1 < ix < ll - 1
                      and token[0] == Token.KW and token[1].upper() in self.pp.go_kw
                      and line[ix + 1][0] == Token.KW and line[ix + 1][1].upper() in self.pp.to_kw
                      and line[ix - 1][0] == Token.KW and line[ix - 1][1].upper() in self.pp.then_kw):
                    skip = True
                elif token[0] != Token.KW or token[1] not in self.pp.let_kw:
                    new_line.append(token)
            rv.append(new_line)
        self.data = rv

    def clean_labs(self):
        # remove all line numbers that are not used as targets
        labels = gettgtlabs(self.data)
        lines = []

        for line in self.data:
            if not line:
                continue
            if line[0][0] != Token.LABEL or (line[0][0] == Token.LABEL and line[0][1].upper() in labels):
                lines.append(line)
            elif len(line) > 1:
                lines.append(line[1:])

        self.data = lines

    def i2x(self):
        self.data = map2d(int2hex, self.data)

    def z2p(self):
        self.data = map2d(zero2pt, self.data)

    def trim_quote(self):
        lines = []
        for line in self.data:
            if line[-1][0] == Token.QUOTED:
                line[-1] = (Token.QUOTED, line[-1][1][:-1])
            lines.append(line)
        self.data = lines

    def opt(self, max_len=0, flags=None):
        if not flags:
            flags = OFlags(0)
        # pack a basic program
        if OFlags.Z2P in flags:
            self.z2p()
        if OFlags.I2X in flags:
            self.i2x()
        self.data = no_ws(self.data)
        self.clean_labs()
        self.no_remarks()
        self.data = reid(self.pp, self.data)
        self.merge_lines(max_len=max_len, text_len=OFlags.TEXTLEN in flags)
        if OFlags.QUOTE in flags:
            self.trim_quote()
        self.data = renumber(self.data, start=0, interval=1)


def split_lines(pp, data=None):
    if not data:
        data = pp.full_parse
    lines = []
    for line in data:
        start = 0
        for ix, field in enumerate(line):
            if field[1].upper() in pp.rem_kw + pp.if_kw:
                break
            if field[0] == ord(':'):
                lines.append(line[start:ix])
                start = ix + 1
        lines.append(line[start:])
    return lines


def get_len(pp, in_line, text_len=False):
    if not in_line:
        return 0
    line = in_line
    if len(line) == 0:
        return 0
    if line[0][0] == Token.LABEL:
        line = line[1:]
    if line and text_len:
        return len(pp.deparse_line(line))
    len_acc = 0
    for token in line:
        if token[0] != Token.KW:
            len_acc += len(token[1])
        elif token[2] < 0x100:
            len_acc += 1
        elif token[2] < 0x10000:
            len_acc += 2
        else:
            len_acc += 3

    return len_acc


def int2hex(token: tuple) -> tuple:
    if token[0] == Token.NUM and 0 <= int(token[1]) < 0x10000:
        return Token.HEX, str(f'&H{int(token[1]):X}')
    return token


def zero2pt(token: tuple) -> tuple:
    if token[0] == Token.NUM and int(token[1]) == 0:
        return Token.FLOAT, '.'
    return token


def map2d(fn, data: [[tuple]]) -> [[tuple]]:
    rv = []
    for line in data:
        rv.append(list(map(fn, line)))
    return rv
