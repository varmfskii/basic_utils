from enum import Flag, auto

from msbasic.labels import gettgtlabs, renumber
from msbasic.parser import Parser
from msbasic.tokens import Token
from msbasic.variables import reid


class OFlags(Flag):
    I2X = auto()
    Z2P = auto()
    QUOTE = auto()
    TEXTLEN = auto()
    FIXDATA = auto()


class Optimizer:
    def __init__(self, parser: Parser, data: [int] or None = None):
        self.pp = parser
        if data:
            self.data = self.pp.parse(data)
        else:
            self.data = parser.full_parse

    def no_remarks(self) -> None:
        # remove all "unnecessary" remarks
        lines = []

        for line in self.data:
            for tix, token in enumerate(line):
                if token.matchkw(self.pp.specials['REM']):
                    if tix > 0 and line[tix - 1].t == ord(':'):
                        line = line[:tix - 1]
                    else:
                        line = line[:tix]
                    break
            if len(line) != 0:
                lines.append(line)

        self.data = lines

    def merge_lines(self, max_len: int = 0, text_len: bool = False) -> None:
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
            if line[0].islabel() or 0 < max_len < old_len + 1 + next_len:
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
                    if len(nextline) > 0 and len(line) > 0:
                        nextline.append(Token.other(':'))
                        old_len += 1
                    nextline += line
                    old_len += next_len
                else:
                    nextline = line
                    old_len = 5 + next_len
            for token in line:
                if token.matchkw(self.pp.specials['IF'] + self.pp.specials['DATA']):
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

    def clean_goto(self) -> None:
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
                elif (1 < ix < ll - 1 and line[ix - 1].matchkw(self.pp.then_kw)
                      and token.matchkw(self.pp.specials['GO'])
                      and line[ix + 1].matchkw(self.pp.specials['TO'])):
                    skip = True
                elif not (token.matchkw(self.pp.specials['LET'])
                          or (ix > 0 and token.matchkw(self.pp.specials['GOTO'])
                              and line[ix - 1].matchkw(self.pp.then_kw))):
                    new_line.append(token)
            rv.append(new_line)
        self.data = rv

    def clean_labs(self) -> None:
        # remove all line numbers that are not used as targets
        labels = gettgtlabs(self.data)
        lines = []

        for line in self.data:
            if not line:
                continue
            if not line[0].islabel() or line[0].v in labels:
                lines.append(line)
            elif len(line) > 1:
                lines.append(line[1:])

        self.data = lines

    def i2x(self) -> None:
        self.data = map2d(int2hex, self.data)

    def z2p(self) -> None:
        self.data = map2d(zero2pt, self.data)

    def trim_quote(self) -> None:
        lines = []
        for line in self.data:
            if line[-1].isquoted():
                line[-1].r = line[-1].r[:-1]
            lines.append(line)
        self.data = lines

    def opt(self, max_len: int = 0, flags: OFlags or None = None) -> None:
        if not flags:
            flags = OFlags(0)
        # pack a basic program
        if OFlags.Z2P in flags:
            self.z2p()
        if OFlags.I2X in flags:
            self.i2x()
        self.clean_labs()
        self.no_remarks()
        self.data = reid(self.pp, self.data)
        self.merge_lines(max_len=max_len, text_len=OFlags.TEXTLEN in flags)
        if OFlags.QUOTE in flags:
            self.trim_quote()
        self.data = renumber(self.data, start=0, interval=1)


def split_lines(pp: Parser, data: [[Token]] or None = None) -> [[Token]]:
    if not data:
        data = pp.full_parse
    lines = []
    for line in data:
        start = 0
        for ix, field in enumerate(line):
            if field.matchkw(pp.specials['REM'] + pp.specials['IF']):
                break
            if field.t == ord(':'):
                lines.append(line[start:ix])
                start = ix + 1
        lines.append(line[start:])
    return lines


def get_len(pp: Parser, in_line: [Token], text_len: bool = False) -> int:
    if not in_line:
        return 0
    line = in_line
    if len(line) == 0:
        return 0
    if line[0].islabel():
        line = line[1:]
    if line and text_len:
        return len(pp.deparse_line(line))
    len_acc = 0
    for token in line:
        if not token.iskw():
            len_acc += len(token.r)
        elif token.v < 0x100:
            len_acc += 1
        elif token.v < 0x10000:
            len_acc += 2
        else:
            len_acc += 3

    return len_acc


def int2hex(token: Token) -> Token:
    if token.isdec() and 0 <= token.v < 0x10000:
        return token.hex(f'&H{token.v:X}')
    return token


def zero2pt(token: Token) -> Token:
    if token.isnum() and token.v == 0:
        return Token.float('.')
    return token


def map2d(fn, data: [[Token]]) -> [[Token]]:
    rv = []
    for line in data:
        rv.append(list(map(fn, line)))
    return rv
