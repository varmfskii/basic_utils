# parse Microsoft BASIC dialects, may be useful for some others
import re
import sys


class Parser:
    # field types
    NONE = 0
    OTHER = 1
    LABEL = 2
    WS = 3
    QUOTED = 4
    NUM = 5
    ID = 6
    LEFT = 7
    RIGHT = 8
    SEP = 9
    # case
    LOWER = -1
    NOCASE = 0
    UPPER = 1

    def __init__(self, keywords, remarks, data=None):
        self.kw2code = {}
        self.code2kw = {}
        self.regexs = [
            (self.WS, re.compile('^( +)')),
            (self.QUOTED, re.compile('^("[^"]*")')),
            (self.NUM, re.compile('^(([0-9]+(\\.[0-9]*)?|\\.[0-9]+)(E[+-]?[0-9]*)?)', flags=re.IGNORECASE)),
            (self.ID, re.compile('^([A-Z][A-Z0-9]*)', flags=re.IGNORECASE)),
            (self.LEFT, re.compile('^(\\()')),
            (self.RIGHT, re.compile('^(\\))')),
            (self.SEP, re.compile('^(:)'))
        ]
        self.label = re.compile('^ *([0-9]+) *')
        for kw, code in keywords:
            self.kw2code[kw.upper()] = code
            self.code2kw[code] = kw
        self.remarks = remarks
        self.match = ""
        self.pos = 0
        self.line_len = 0
        self.full_parse = []
        if data is not None:
            for line in data.split('\n'):
                self.parse_line(line)

    def matcher(self, regexp, string):
        match = regexp.match(string)
        if not match:
            return False
        self.match = match[1]
        self.pos += len(match[0])
        return True

    def parse_line(self, line):
        self.pos = 0
        self.line_len = len(line)
        other = ""
        if self.matcher(self.label, line):
            parsed = [(self.LABEL, self.match)]
        else:
            parsed = []
        while self.pos < self.line_len:
            self.match = ""
            code = self.NONE
            for kw in self.kw2code.keys():
                kwl = len(kw)
                if self.pos + kwl <= self.line_len and kw.upper() == line[self.pos:self.pos + kwl].upper():
                    self.match = line[self.pos:self.pos + kwl]
                    self.pos += kwl
                    code = self.kw2code[kw]
                    if self.match.upper() in self.remarks:
                        if other != "":
                            parsed.append((self.OTHER, other))
                            other = ""
                        parsed.append((code, self.match))
                        self.match = ""
                        if self.pos != self.line_len:
                            parsed.append((self.OTHER, line[self.pos:]))
                            self.pos = self.line_len
                    break
            if self.match == "":
                for regex in self.regexs:
                    if self.matcher(regex[1], line[self.pos:]) and self.match != "":
                        code = regex[0]
                        break
            if self.match != "":
                if other != "":
                    parsed.append((self.OTHER, other))
                    other = ""
                parsed.append((code, self.match))
            elif self.pos < self.line_len:
                other += line[self.pos]
                self.pos += 1
        if other != "":
            parsed.append((self.OTHER, other))
        if parsed:
            self.full_parse.append(parsed)
        return parsed

    def no_ws(self):
        rv = []
        for line in self.full_parse:
            new_line = []
            for val in line:
                if val[0] != self.WS:
                    new_line.append(val)
            rv.append(new_line)
        return rv

    def deparse(self, ws=False, case=UPPER):
        out = ""
        for line in self.full_parse:
            if len(line) == 0:
                continue
            if line[0][0] != self.LABEL:
                out += '   '
            for ix, (typ, ent) in enumerate(line):
                if case == self.UPPER and typ != self.QUOTED:
                    ent = ent.upper()
                elif case == self.LOWER and typ != self.QUOTED:
                    ent = ent.lower()
                if ws and ent[0].isalnum() and out and out[-1].isalnum():
                    ent = ' ' + ent
                elif typ == self.LABEL or (
                        not ws and typ == self.ID and ix + 1 < len(line) and line[ix + 1][1][0].isalpha()):
                    ent += ' '
                out += ent
            out += "\n"
        return out


if __name__ == "__main__":
    sys.stderr.write("This is a library")
