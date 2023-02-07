# parse Microsoft BASIC dialects, may be useful for some others
import re
import sys


class Parser:
    # field types
    NONE = 256
    OTHER = 257
    LABEL = 258
    WS = 259
    QUOTED = 260
    NUM = 261
    ID = 262
    DATA = 263
    REMARK = 264
    COMMA = ord(',')
    LEFT = ord('(')
    RIGHT = ord(')')
    SEP = ord(':')
    STR = ord('$')

    # case
    LOWER = -1
    NOCASE = 0
    UPPER = 1

    def __init__(self, opts, data=None):
        keywords = opts.keywords
        remarks = opts.remarks
        self.isdragon = opts.isdragon
        self.disk = opts.disk
        self.address = opts.address
        self.kw2code = {}
        self.code2kw = {}
        self.regexs = [
            (0, re.compile(r'[(),$:]')),
            (self.WS, re.compile(' +')),
            (self.QUOTED, re.compile('"[^"]*"')),
            (self.NUM, re.compile(r'([0-9]+(\.[0-9]*)?|\.[0-9]+)(E[+-]?[0-9]+)?|&H[0-9A-F]+', flags=re.IGNORECASE)),
            (self.ID, re.compile('[A-Z][A-Z0-9]*', flags=re.IGNORECASE))
        ]
        self.label = re.compile(' *([0-9]+)')
        for kw, code in keywords:
            self.kw2code[kw.upper()] = code
            self.code2kw[code] = kw
        self.remarks = remarks
        self.ms = []
        for k in ['CLOAD', 'CSAVE', 'DLOAD', 'LOAD', 'SAVE']:
            if k in self.kw2code.keys():
                self.ms.append(self.kw2code[k])
        self.full_parse = []
        if data is not None:
            if data[0] < 0x80 and data[1] < 0x80:
                data = "".join(map(chr, data))
                for line in re.split('[\n\r]+', data):
                    parse = self.parse_line(line)
                    if parse:
                        self.full_parse.append(parse)
            elif data[0] == 0xff:
                self.full_parse = self.parse_bin(data[3:])
            elif data[0] == 0x55:
                self.full_parse = self.parse_bin(data[9:])
            else:
                self.full_parse = self.parse_bin(data)

    def parse_line(self, line):
        match = self.label.match(line)
        if match:
            parsed = [(self.LABEL, line[:match.end()])]
            line = line[match.end():]
        else:
            parsed = []
        return parsed + self.parse_txt(line)

    def parse_txt(self, line):
        parsed = []
        while line != "":
            ml, match = self.match_kw(line)
            if match:
                # print(match)
                line = line[ml:]
                parsed.append(match)
                if match[0] == self.kw2code['DATA']:
                    m = re.match('[^:]+', line)
                    if m:
                        parsed.append((self.DATA, line[:m.end()]))
                        line = line[m.end():]
                if self.code2kw[match[0]] in self.remarks:
                    parsed.append((self.REMARK, line))
                    line = ""
                continue
            ml, match = self.match_re(line)
            if match:
                # print(match)
                line = line[ml:]
                parsed.append(match)
                continue

            parsed.append((self.OTHER, line[0]))
            line = line[1:]

        # print(parsed)
        tokens = parsed[:1]
        for token in parsed[1:]:
            if tokens[-1][0] == self.OTHER and token[0] == self.OTHER:
                tokens[-1] = (self.OTHER, tokens[-1][1] + token[1])
            elif token[0] == self.ID and token[1][0].upper() == 'M' and (
                    (len(tokens) >= 1 and tokens[-1][0] in self.ms) or
                    (len(tokens) >= 2 and tokens[-1][0] == self.WS and tokens[-2][0] in self.ms)):
                tokens.append((self.OTHER, token[1][0]))
                if len(token[1]) > 1:
                    tokens.append((self.ID, token[1][1:]))
            else:
                tokens.append(token)

        # print(tokens)
        return tokens

    def match_kw(self, line):
        ll = len(line)
        for kw in self.kw2code.keys():
            kl = len(kw)
            if ll >= kl and kw == line[:kl].upper():
                return kl, (self.kw2code[kw], line[:kl])
        return 0, None

    def match_re(self, line):
        for (code, regex) in self.regexs:
            match = regex.match(line)
            if match:
                if code == 0 and match.end() == 1:
                    return 1, (ord(line[0]), line[0])
                else:
                    return match.end(), (code, line[:match.end()])
        return 0, None

    def no_ws(self):
        rv = []
        for line in self.full_parse:
            new_line = []
            for val in line:
                if val[0] != self.WS:
                    new_line.append(val)
            rv.append(new_line)
        return rv

    def parse_bin(self, data):
        parsed = []
        while len(data) >= 4 and (data[0] != 0 or data[1] != 0):
            line = [(self.LABEL, str(data[2] * 0x100 + data[3]))]
            data = data[4:]
            while len(data) >= 2 and data[0] != 0:
                code2 = data[0] * 0x100 + data[1]
                code1 = data[0]
                if code2 in self.code2kw.keys():
                    line.append((code2, self.code2kw[code2]))
                    data = data[2:]
                elif code1 in self.code2kw.keys():
                    line.append((code1, self.code2kw[code1]))
                    data = data[1:]
                elif code1 < 0x80:
                    text = ""
                    ix = 0
                    while 0x20 <= data[ix] < 0x80 and data[ix + 1] != 0x83:
                        text += chr(data[ix])
                        ix += 1
                    data = data[len(text):]
                    line += self.parse_txt(text)
                else:
                    sys.stderr.write('Malformed file')
            parsed.append(line)
            data = data[1:]
        return parsed

    def deparse(self, ws=False, case=UPPER):
        out = ""
        for line in self.full_parse:
            if len(line) == 0:
                continue
            if line[0][0] != self.LABEL:
                out += ' '
            for ix, (typ, ent) in enumerate(line):
                if case == self.UPPER and typ != self.QUOTED:
                    ent = ent.upper()
                elif case == self.LOWER and typ != self.QUOTED:
                    ent = ent.lower()
                if ws and ent[0].isalnum() and out and out[-1].isalnum():
                    ent = ' ' + ent
                elif typ == self.LABEL and ix + 1 < len(line) and line[ix + 1][0] != self.WS:
                    ent += ' '
                out += ent
            out += "\n"
        return out


if __name__ == "__main__":
    sys.stderr.write("This is a library")
