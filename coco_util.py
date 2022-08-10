import parser
from coco_sdecb import keywords, remarks


def tokenize_line(line):
    tokens = []
    for token in line:
        if token[0] == parser.LABEL:  # line number
            val = int(token[1])
            tokens += [val // 256, val & 0xff]
        elif token[0] > 255:  # tokenized extended keyword
            val = token[0]
            tokens += [val // 256, val & 0xff]
        elif token[0] > 127:  # tokenized keyword
            tokens.append(token[0])
        elif token[0] == parser.QUOTED or token[0] == parser.OTHER:  # explicit text
            for char in token[1]:
                tokens.append(ord(char))
        else:
            for char in token[1].upper():  # code text, interpreter only recognizes uppercase
                tokens.append(ord(char))
    tokens.append(0)
    return tokens


def tokenize(data, ws=False, disk=True):
    pp = parser.Parser(keywords, remarks, data)
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    address = 0x2601
    for line in parsed:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 256, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if disk:
        val = len(tokenized)
        tokenized = [255, val // 256, val & 0xff] + tokenized
    return bytearray(tokenized)


def tokenize_file(iname, oname, ws=False, disk=True):
    open(oname, 'wb').write(tokenize(open(iname, 'r').read(), ws=ws, disk=disk))
