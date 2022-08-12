# parse Microsoft BASIC dialects, may be useful for some others
import re
import sys

NONE = -1
OTHER = 0
LABEL = 1
WS = 2
QUOTED = 3
NUM = 4
ID = 5
LEFT = 6
RIGHT = 7
SEP = 8


class Parser:

    def __init__(self, keywords, remarks, data=None):
        self.kw2code = {}
        self.code2kw = {}
        self.regexs = [
            (WS, re.compile('^( +)')),
            (QUOTED, re.compile('^("[^"]*")')),
            (NUM, re.compile('^(([0-9]+(\\.[0-9]*)?|\\.[0-9]+)(E[+-]?[0-9]*)?)', flags=re.IGNORECASE)),
            (ID, re.compile('^([A-Z][A-Z0-9]*)', flags=re.IGNORECASE)),
            (LEFT, re.compile('^(\\()')),
            (RIGHT, re.compile('^(\\))')),
            (SEP, re.compile('^(:)'))
        ]
        self.label = re.compile('^ *([0-9]+) *')
        for kw in keywords:
            self.kw2code[kw[0]] = kw[1]
            self.code2kw[kw[1]] = kw[0]
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
            parsed = [(LABEL, self.match)]
        else:
            parsed = []
        while self.pos < self.line_len:
            self.match = ""
            code = NONE
            for kw in self.kw2code.keys():
                kwl = len(kw)
                if self.pos + kwl <= self.line_len and kw.upper() == line[self.pos:self.pos + kwl].upper():
                    self.match = line[self.pos:self.pos + kwl]
                    self.pos += kwl
                    code = self.kw2code[kw]
                    if self.match.upper() in self.remarks:
                        if other != "":
                            parsed.append((OTHER, other))
                            other = ""
                        parsed.append((code, self.match))
                        self.match = ""
                        if self.pos != self.line_len:
                            parsed.append((OTHER, line[self.pos:]))
                            self.pos = self.line_len
                    break
            if self.match == "":
                for regex in self.regexs:
                    if self.matcher(regex[1], line[self.pos:]) and self.match != "":
                        code = regex[0]
                        break
            if self.match != "":
                if other != "":
                    parsed.append((OTHER, other))
                    other = ""
                parsed.append((code, self.match))
            elif self.pos < self.line_len:
                other += line[self.pos]
                self.pos += 1
        if other != "":
            parsed.append((OTHER, other))
        if parsed:
            self.full_parse.append(parsed)
        return parsed

    def no_ws(self):
        rv = []
        for line in self.full_parse:
            new_line = []
            for val in line:
                if val[0] != WS:
                    new_line.append(val)
            rv.append(new_line)
        return rv

    @staticmethod
    def deparse(lines):
        out = ""
        for line in lines:
            for ix, field in enumerate(line):
                out += field[1].upper()
                if field[0] == LABEL or (
                        field[0] == ID and ix + 1 < len(line) and line[ix + 1][1][0].isalpha()):
                    out += " "
            out += "\n"
        return out

    def pack(self):
        return self.deparse(self.no_ws())


if __name__ == "__main__":
    sys.stderr.write("This is a library")
