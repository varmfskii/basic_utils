#!/usr/bin/env python3
import sys
import re
from basic69.coco import sdecb

class Parser:
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
    
    code2kw = {}
    kw2code = {}
    full_parse = None
    rem_codes = []
    
    def __init__(self, keywords, remarks, data=None, be=True):
        self.be = be
        for (w, c) in keywords:
            self.code2kw[c]=w
            self.kw2code[w]=c
        if data:
            self.parse(data)
        for rem in remarks:
            self.rem_codes.append(self.kw2code[rem])

    def parse(self, data):
        if data[0]==0xff:
            self.full_parse = self.parse_bin(data[3:])
        elif data[0]==0x55 and data[1]==0:
            self.full_parse = self.parse_bin(data[9:])
        elif data[0]<128 and data[1]<128:
            self.full_parse = self.parse_txt("".join(map(chr, data)))
        else:
            self.full_parse = self.parse_bin(data)
        return self.full_parse
    
    def parse_bin(self, data):
        parsed = []
        while(data[0]!=0 or data[1]!=0):
            data = data[2:]
            if self.be:
                line = [(self.LABEL, str(data[0]*0x100+data[1]))]
            else:
                line = [(self.LABEL, str(data[0]+data[1]*0x100))]
            data = data[2:]
            while data[0]!=0:
                c1 = data[0]
                if len(data)>1:
                    c2 = c1*0x100+data[1]
                else:
                    c2 = c1*0x100
                if len(data)>2:
                    c3 = c2*0x100+data[2]
                else:
                    c3 = c2*0x100
                if line[-1][0] in self.rem_codes:
                    rem = ''
                    while data[0]!=0:
                        rem += chr(data[0])
                        data = data[1:]
                    if rem!='':
                        line.append((self.REM, rem))
                elif line[-1][0] == self.kw2code['DATA']:
                    data_data = ''
                    while data[0]!=0 and data[0]!=ord(':'):
                        data_data += chr(data[0])
                        data = data[1:]
                    if data!='':
                        line.append((self.DATA, data_data))
                elif c3 in self.code2kw.keys():
                    # 3-byte token
                    data = data[3:]
                    line.append((c3, self.code2kw[c3]))
                elif c2 in self.code2kw.keys():
                    # 2-byte token
                    data = data[2:]
                    line.append((c2, self.code2kw[c2]))
                elif c1 in self.code2kw.keys():
                    # 1-byte token
                    data = data[1:]
                    line.append((c1, self.code2kw[c1]))
                elif 'A'<=chr(c1)<='Z' or 'a'<=chr(c1)<='z':
                    # id
                    id=''
                    while '0'<=chr(c1)<='9' or 'A'<=chr(c1)<='Z' or 'a'<=chr(c1)<='z':
                        id+=chr(data[0])
                        data=data[1:]
                        c1 = data[0]
                    line.append((self.ID, id))
                elif c1==ord('"'):
                    # quoted
                    quote = '"'
                    data=data[1:]
                    while data[0]!=0 and data[0]!=ord('"'):
                        quote += chr(data[0])
                        data=data[1:]
                    if data[0]!=0:
                        quote += '"'
                        data=data[1:]
                        line.append((self.QUOTED, quote))
                elif line[-1][0]==self.NONE:
                    data = data[1:]
                    line[-1] = (self.NONE, line[-1][1]+chr(c1))
                else:
                    data = data[1:]
                    line.append((self.NONE, chr(c1)))
            data = data[1:]
            parsed.append(self.pass2(line))
        return parsed
    
    def pass2(self, line):
        tokens = []
        for (c, w) in line:
            if c==self.NONE:
                tokens += self.split_none(w)
            else:
                tokens.append((c, w))

        nows = self.nows(tokens)
        nl = len(nows)
        for ix, token in enumerate(nows):
            (c, w) = token
            if c==self.ID:
                if ix+2<len(nows) and nows[ix+1][0]==ord('$') and nows[ix+2][0]==ord('('):
                    nows[ix] = (self.STRARR, w)
                elif ix+1<len(nows) and nows[ix+1][0]==ord('$'):
                    nows[ix] = (self.STR, w)
                elif ix+1<len(nows) and nows[ix+1][0]==ord('('):
                    nows[ix] = (self.ARR, w)

        i=0
        j=0
        while i<len(tokens):
            if tokens[i][0]==self.WS:
                i += 1
            else:
                tokens[i] = nows[j]
                i += 1
                j += 1

        return tokens

    def split_none(self, word):
        tokens = []
        while word!='':
            match = re.match('[0-9]*\.[0-9]*', word)
            if match and match.end()>0:
                ml = match.end()
                tokens.append((self.FLOAT, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('[0-9]*(\.[0-9]*)?[+-]?[Ee][0-9]*', word)
            if match and match.end()>0:
                ml = match.end()
                tokens.append((self.FLOAT, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('[0-9]*', word)
            if match and match.end()>0:
                ml = match.end()
                tokens.append((self.NUM, word[:ml]))
                word = word[ml:]
                continue
            match = re.match('&H[0-9A-Fa-f]*', word)
            if match and match.end()>0:
                ml = match.end()
                tokens.append((self.HEX, word[:ml]))
                word = word[ml:]
                continue
            match = re.match(' *', word)
            if match and match.end()>0:
                ml = match.end()
                tokens.append((self.WS, word[:ml]))
                word = word[ml:]
                continue
            tokens.append((ord(word[0]), word[0]))
            word = word[1:]
        return tokens


    def nows(self, tokens):
        rv = []
        for token in tokens:
            if token[0]!=self.WS:
                rv.append(token)
        return rv
    
    def parse_txt(self, data, be=True):
        parsed = []
        for linein in re.split('[\n\r]+', data):
            if linein=="":
                continue
            match = re.match(' *[0-9]+ *', linein)
            if match:
                line = [(self.LABEL, str(int(linein[:match.end()])))]
                lineom = linein[match.end():]
            else:
                line = []
            match = re.match(' *', linein)
            linein = linein[match.end():]
            while linein!='':
                if len(line)>0:
                    if line[-1][0] in self.rem_codes:
                        line.append((self.REM, linein))
                        linein = ''
                        continue
                    if line[-1][0] == self.kw2code['DATA']:
                        match = re.match('[^:]+', linein)
                        if match:
                            ml = match.end()
                            line.append((self.DATA, linein[:ml]))
                            linein = linein[ml:]
                        continue
                            
                found = False
                for kw in self.kw2code.keys():
                    kl = len(kw)
                    if linein[:kl].upper()==kw:
                        found = True
                        line.append((self.kw2code[kw], linein[:kl]))
                        linein = linein[kl:]
                        break
                if found:
                    continue
                
                match = re.match('[A-Za-z][0-9A-Za-z]*', linein)
                if match:
                    ml = match.end()
                    line.append((self.ID, linein[:ml]))
                    linein = linein[ml:]
                    continue

                match = re.match('"[^"]*"', linein)
                if match:
                    ml = match.end()
                    line.append((self.QUOTED, linein[:ml]))
                    linein = linein[ml:]
                    continue
                
                if line[-1][0]==self.NONE:
                    line[-1] = (self.NONE, line[-1][1]+linein[0])
                else:
                    line.append((self.NONE, linein[0]))
                linein = linein[1:]
            parsed.append(self.pass2(line))
        return parsed

pp = Parser(sdecb.keywords, sdecb.remarks)

for fn in sys.argv[1:]:
    data = open(fn, "rb").read()
    parsed = pp.parse(data)
    for line in parsed:
        print(line)
