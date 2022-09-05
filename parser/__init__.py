# parse Microsoft BASIC dialects, may be useful for some others
import re
import sys
from enum import Enum


class Types(Enum):
    # field types
    NONE = (0, None)
    OTHER = (1, None)
    LABEL = (2, None)
    WS = (3, '^( +)')
    QUOTED = (4, '^("[^"]*")')
    NUM = (5, '^(([0-9]+(\\.[0-9]*)?|\\.[0-9]+)(E[+-]?[0-9]*)?|&H[0-9A-F]+)')
    ID = (6, '^([A-Z][A-Z0-9]*)')
    LEFT = (7, '^(\\()')
    RIGHT = (8, '^(\\))')
    SEP = (9, '^(:)')

    def __init__(self, ix, regex):
        self.ix = ix
        if regex:
            self.regex = re.compile(regex, flags=re.IGNORECASE)
        else:
            self.regex = None

    def match(self, string):
        if self.regex:
            return self.regex.match(string)
        else:
            return None


class Parser:
    # case
    LOWER = -1
    NOCASE = 0
    UPPER = 1

    def __init__(self, dialect, data=None):
        keywords, special, isdragon, do_special = dialect
        self.kw2code = {}
        self.code2kw = {}
        self.regexs = [
            (Types.WS, re.compile('^( +)')),
            (Types.QUOTED, re.compile('^("[^"]*")')),
            (Types.NUM,
             re.compile('^(([0-9]+(\\.[0-9]*)?|\\.[0-9]+)(E[+-]?[0-9]*)?|&H[0-9A-F]+)', flags=re.IGNORECASE)),
            (Types.ID, re.compile('^([A-Z][A-Z0-9]*)', flags=re.IGNORECASE)),
            (Types.LEFT, re.compile('^(\\()')),
            (Types.RIGHT, re.compile('^(\\))')),
            (Types.SEP, re.compile('^(:)'))
        ]
        self.LABEL = re.compile('^ *([0-9]+) *')
        for kw, code in keywords:
            self.kw2code[kw.upper()] = code
            self.code2kw[code] = kw
        self.special = list(map(lambda x: self.kw2code[x], special))
        if do_special:
            self.do_special = do_special
        else:
            self.do_special = self.do_rems
        self.match = ""
        self.pos = 0
        self.line_len = 0
        self.full_parse = []
        if data is not None:
            for line in data.split('\n'):
                self.parse_line(line)

    def matcher(self, atype, string):
        match = atype.match(string)
        if match:
            self.match = match[1]
            self.pos += len(match[0])
        return match

    def parse_line(self, line):
        self.pos = 0
        self.line_len = len(line)
        other = ""
        if self.matcher(self.LABEL, line):
            parsed = [(Types.LABEL, self.match)]
        else:
            parsed = []
        while self.pos < self.line_len:
            code = Types.NONE
            for kw in self.kw2code.keys():
                kwl = len(kw)
                if self.pos + kwl <= self.line_len and kw.upper() == line[self.pos:self.pos + kwl].upper():
                    self.match = line[self.pos:self.pos + kwl]
                    self.pos += kwl
                    code = self.kw2code[kw]
                    break
            if code == Types.NONE:
                for atype in Types:
                    if self.matcher(atype, line[self.pos:]) and self.match != "":
                        code = atype
                        break
            if code != Types.NONE:
                if other != "":
                    parsed.append((Types.OTHER, other))
                    other = ""
                parsed.append((code, self.match))
                if code in self.special:
                    parsed = self.do_special(self, code, parsed, line)
            elif self.pos < self.line_len:
                other += line[self.pos]
                self.pos += 1
        if other != "":
            parsed.append((Types.OTHER, other))
        if parsed:
            self.full_parse.append(parsed)
        return parsed

    # noinspection PyUnusedLocal
    @staticmethod
    def do_rems(parent, code, parsed, line):
        if parent.pos != parent.line_len:
            parsed.append((Types.OTHER, line[parent.pos:]))
            parent.pos = parent.line_len
        return parsed

    def no_ws(self):
        rv = []
        for line in self.full_parse:
            new_line = []
            for val in line:
                if val[0] != Types.WS:
                    new_line.append(val)
            rv.append(new_line)
        return rv

    def deparse(self, ws=False, case=UPPER):
        out = ""
        for line in self.full_parse:
            if len(line) == 0:
                continue
            if line[0][0] != Types.LABEL:
                out += '   '
            for ix, (typ, ent) in enumerate(line):
                if case == self.UPPER and typ != Types.QUOTED:
                    ent = ent.upper()
                elif case == self.LOWER and typ != Types.QUOTED:
                    ent = ent.lower()
                if ws and ent[0].isalnum() and out and out[-1].isalnum():
                    ent = ' ' + ent
                elif typ == Types.LABEL or (
                        not ws and typ == Types.ID and ix + 1 < len(line) and line[ix + 1][1][0].isalpha()):
                    ent += ' '
                out += ent
            out += "\n"
        return out


if __name__ == "__main__":
    sys.stderr.write("This is a library")
