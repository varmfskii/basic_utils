#!/usr/bin/env python3
import re

from msbasic.options import Options
from msbasic.tokens import Token, TokenType


class Parser:
    __version__ = 'msbasic 240122'
    spacer = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"')
    full_parse = None

    @staticmethod
    def version():
        return [f'Parser:\t{Parser.__version__}']

    def __init__(self, opts: Options, data: [int] or None = None, be=True, fix_data=False, onepass=False):
        self.be = be
        self.code2kw = opts.dialect.code2kw
        self.kw2code = opts.dialect.kw2code
        self.kw_keys = opts.dialect.kw_keys
        self.specials = opts.dialect.specials
        self.then_kw = self.specials['THEN'] + self.specials['ELSE']
        self.branch_kw = self.specials['GO'] + self.specials['GOTO'] + self.specials['GOSUB']
        self.ign_kw = self.specials['TO'] + self.specials['SUB']
        self.gen = Token(m=opts.dialect.kw2code)
        self.preserve = opts.dialect.preserve
        if data:
            self.parse(data, fix_data=fix_data, onepass=onepass)

    def parse(self, data: [int], fix_data=False, onepass=False) -> [[Token]]:
        binary = False
        for d in data:
            if d == 0:
                binary = True
                break
        if binary:
            self.full_parse = self.kws_bin(data)
        else:
            self.full_parse = self.kws_txt(data)
        if onepass:
            return self.full_parse
        return self.get_tokens(fix_data=fix_data)

    def kws_bin(self, data: [int]) -> [[Token]]:
        parsed = []
        while len(data) >= 2 and data[0] or data[1]:
            if self.be:
                v = data[2] * 0x0100 + data[3]
            else:
                v = data[2] * 0x0100 + data[3]
            tokens = [self.gen.label(str(v))]
            data = data[4:]
            while data[0]:
                # remark
                if len(tokens) and tokens[-1].matchkw(self.specials['REM']):
                    remark = ''
                    while data[0]:
                        remark += chr(data[0])
                        data = data[1:]
                    tokens.append(self.gen.rem(remark))
                    continue
                # data statement
                if len(tokens) and tokens[-1].matchkw(self.specials['DATA']):
                    data_data = ''
                    while data[0] and data[0] != ord(':'):
                        data_data += chr(data[0])
                        data = data[1:]
                    if data_data:
                        tokens.append(self.gen.data(data_data))
                    continue
                # tokenized keyword
                c1 = data[0]
                if len(data) > 1:
                    c2 = c1 * 0x100 + data[1]
                else:
                    c2 = c1 * 0x100
                if len(data) > 2:
                    c3 = c2 * 0x100 + data[2]
                else:
                    c3 = c2 * 0x100
                if c3 in self.code2kw.keys():
                    # 3-byte token
                    data = data[3:]
                    tokens.append(self.gen.kw(self.code2kw[c3]))
                    continue
                if c2 in self.code2kw.keys():
                    # 2-byte token
                    data = data[2:]
                    tokens.append(self.gen.kw(self.code2kw[c2]))
                    continue
                if c1 in self.code2kw.keys():
                    # 1-byte token
                    data = data[1:]
                    tokens.append(self.gen.kw(self.code2kw[c1]))
                    continue
                # quoted string
                if data[0] == ord('"'):
                    quoted = '"'
                    data = data[1:]
                    while data[0] != 0 and data[0] != ord('"'):
                        quoted += chr(data[0])
                        data = data[1:]
                    if data[0] == ord('"'):
                        quoted += '"'
                        data = data[1:]
                    tokens.append(self.gen.quoted(quoted))
                    continue
                # potential id
                next_chr = chr(data[0])
                if 'A' <= next_chr <= 'Z' or 'a' <= next_chr <= 'z':
                    datum = ''
                    while ('0' <= next_chr <= '9' or
                           'A' <= next_chr <= 'Z' or
                           'a' <= next_chr <= 'z'):
                        datum += next_chr
                        data = data[1:]
                        next_chr = chr(data[0])
                    if len(tokens) and tokens[-1].isnone():
                        tokens[-1].none_append(datum)
                    else:
                        tokens.append(self.gen.none(datum))
                    continue
                # other
                if len(tokens) and tokens[-1].isnone():
                    tokens[-1].none_append(chr(data[0]))
                else:
                    tokens.append(self.gen.none(chr(data[0])))
                data = data[1:]
            data = data[1:]
            if tokens:
                parsed.append(tokens)
        return parsed

    def get_tokens(self, data: [[Token]] or None = None, fix_data=False) -> [[Token]]:
        if not data:
            data = self.full_parse
        parsed = []
        data_data = []
        for line in data:
            new_line = []
            for token in line:
                if token.isnone():
                    new_line += self.parse_none(token.v)
                elif fix_data and token.isdata():
                    data_data += token.v
                    if len(new_line) >= 2 and new_line[-2].t == ord(':'):
                        new_line = new_line[:-2]
                    else:
                        new_line = new_line[:-1]
                elif not fix_data or not token.matchkw(self.specials['DATA']):
                    new_line.append(token)
            if new_line:
                label = 0
                for ix, token in enumerate(new_line):
                    # adjust to labels where applicable
                    if (label and token.isdec()) or (label == 2 and token.isvar()):
                        new_line[ix] = self.gen.label(token.r)
                    # setup for label detection
                    if token.matchkw(self.then_kw):
                        label = 1
                    elif token.matchkw(self.branch_kw):
                        label = 2
                    elif label == 1 or (label == 2 and token.t not in [TokenType.NUMVAR, TokenType.DEC, ord(',')]
                                        and not token.matchkw(self.ign_kw)):
                        label = 0
                    else:
                        pass
                parsed.append(new_line)
        if data_data:
            parsed.append([self.gen.kw('DATA'), self.gen.data_list(data_data)])
        self.full_parse = parsed
        return self.full_parse

    @staticmethod
    def parse_none(data: str) -> [Token]:
        data = re.sub(' ', '', data).upper()
        tokens = []
        while data != '':
            match = re.match(r'[A-Z][0-9A-Z]*\$\(', data)
            if match:
                tokens += [Token.strarr(match.group(0)[:-2]), Token.other('$'), Token.other('(')]
                data = data[match.end():]
                continue
            match = re.match(r'[A-Z][0-9A-Z]*\$', data)
            if match:
                tokens += [Token.strvar(match.group(0)[:-1]), Token.other('$')]
                data = data[match.end():]
                continue
            match = re.match(r'[A-Z][0-9A-Z]*\$', data)
            if match:
                tokens += [Token.numarr(match.group(0)[:-1]), Token.other('(')]
                data = data[match.end():]
                continue
            match = re.match(r'[A-Z][0-9A-Z]*', data)
            if match:
                tokens.append(Token.numvar(match.group(0)))
                data = data[match.end():]
                continue
            match = re.match(r'&H[0-9A-F]*', data)
            if match:
                tokens.append(Token.hex(match.group(0)))
                data = data[match.end():]
                continue
            match = re.match(r'[0-9]*\.[0-9]*(E[+-]?[0-9]*)', data)
            if match:
                tokens.append(Token.float(match.group(0)))
                data = data[match.end():]
                continue
            match = re.match(r'[0-9]+', data)
            if match:
                tokens.append(Token.dec(match.group(0)))
                data = data[match.end():]
                continue
            tokens.append(Token.other(data[0]))
            data = data[1:]
        return tokens

    def kws_txt(self, data_i: [int]) -> [[Token]]:
        parsed = []
        data = cont_line("".join(map(chr, data_i)))
        for linein in re.split('[\n\r]+', data):
            if linein == "":
                continue
            match1 = re.match(' *([0-9]+) *', linein)
            match2 = re.match(' *_([A-Za-z][0-9A-Za-z]*) *', linein)
            if match1:
                line = [self.gen.label(match1.group(1))]
                linein = linein[match1.end():]
            elif match2:
                line = [self.gen.label(match2.group(1))]
                linein = linein[match2.end():]
            else:
                line = []
                match = re.match(' *', linein)
                linein = linein[match.end():]
            while linein != '':
                if len(line) and line[-1].matchkw(self.specials['REM']):
                    line.append(self.gen.rem(linein))
                    linein = ''
                    continue
                if len(line) and line[-1].matchkw(self.specials['DATA']):
                    match = re.match('[^:]+', linein)
                    if match:
                        line.append(self.gen.data(match.group(0)))
                        linein = linein[match.end():]
                    continue

                kw = self.match_kw(linein)
                if kw:
                    linein = linein[len(kw.r):]
                    line.append(kw)
                    continue

                match = re.match('"[^"]*"?', linein)
                if match:
                    ml = match.end()
                    quoted = linein[:ml]
                    if quoted[-1] != '"':
                        quoted += '"'
                    line.append(self.gen.quoted(quoted))
                    linein = linein[ml:]
                    continue

                match = re.match('.|([A-Za-z][0-9A-Za-z]*)', linein)
                if len(line) and line[-1].isnone():
                    line[-1].none_append(match.group(0))
                else:
                    line.append(self.gen.none(match.group(0)))
                linein = linein[match.end():]
            parsed.append(line)
        return parsed

    @staticmethod
    def split_none(s: str) -> [Token]:
        tokens = []
        while s != '':
            match = re.match('[0-9]*\\.[0-9]*', s)
            if match and match.end() > 0:
                tokens.append(Token.float(match.group(0)))
                s = s[match.end():]
                continue
            match = re.match('[0-9]*(\\.[0-9]*)?[+-]?[Ee][0-9]*', s)
            if match and match.end() > 0:
                tokens.append(Token.float(match.group(0)))
                s = s[match.end():]
                continue
            match = re.match('[0-9]*', s)
            if match and match.end() > 0:
                tokens.append(Token.dec(match.group(0)))
                s = s[match.end()]
                continue
            match = re.match('&H[0-9A-Fa-f]*', s)
            if match and match.end() > 0:
                tokens.append(Token.hex(match.group(0)))
                s = s[match.end():]
                continue
            match = re.match(' *', s)
            if match and match.end() > 0:
                tokens.append(Token.ws(match.group(0)))
                s = s[match.end():]
                continue
            tokens.append(Token.other(s[0]))
            s = s[1:]
        return tokens

    def match_kw(self, line) -> tuple or None:
        ll = len(line)
        for kw in self.kw_keys:
            kl = len(kw)
            if ll >= kl and kw == line[:kl].upper():
                return self.gen.kw(kw.upper())
        return None

    def deparse(self, data=None, ws=False) -> str:
        out = ''
        if not data:
            data = self.full_parse
        for line in data:
            out += self.deparse_line(line, ws=ws) + '\n'
        return out

    def deparse_line(self, line: [Token], ws=False) -> str:
        if line[0].islabel():
            out = line[0].r + ' '
            line = line[1:]
        else:
            out = ' '
        for ix, token in enumerate(line):
            if ((token.iskw() and token.r[0].isalpha() and ix > 0 and line[ix - 1].isvar())
                    or (ws and out[-1] in self.spacer and token.r[0].isalnum())):
                out += ' '
            out += token.r
        return out


def cont_line(data: str) -> str:
    data = data.split('\\')
    s = data[0]
    for p in data[1:]:
        m = re.match('\r?\n?', p)
        if m.end() == 0:
            s += '\\' + p
        else:
            s += p[m.end():]
    return s
