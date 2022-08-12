import parser
from coco.coco import sdecb
from coco.dragon import ddos
from coco.getoptions import isdragon


def tokenize_line(line):
    # convert a parsed line into the tokenized format for a BASIC file
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


def tokenize(pp, ws=False, disk=True):
    # convert a parsed file into tokenized BASIC file
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    if isdragon:
        address = 0x2401
    elif disk:
        address = 0x2601
    else:
        address = 0x25fe
    for line in parsed:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 0x100, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if isdragon:
        val = len(tokenized)
        tokenized = [0x55, 0x01, 0x24, 0x01, val // 256, val & 0xff, 0x8b, 0x8d, 0xaa] + tokenized
    elif disk:
        val = len(tokenized)
        tokenized = [0xff, val // 0x100, val & 0xff] + tokenized
    return bytearray(tokenized)


def detokenize(data):
    data = list(data)
    listing = ""

    if data[0] == 0x55:
        ix = 9
        pp = parser.Parser(ddos.keywords, ddos.remarks)
    elif data[0] == 0xff:
        ix = 3
        pp = parser.Parser(sdecb.keywords, sdecb.remarks)
    else:
        ix = 0
        pp = parser.Parser(sdecb.keywords, sdecb.remarks)

    while data[ix] != 0x00 or data[ix + 1] != 0x00:
        line = f'{data[ix + 2] * 0x100 + data[ix + 3]} '
        ix += 4
        lastid = False
        while data[ix] != 0x00:
            if data[ix] < 0x80:
                if 65 <= data[ix] <= 90:
                    # A-Z
                    lastid = True
                elif data[ix] < 48 or data[ix] > 57:
                    # not 0-9
                    lastid = False
                line += chr(data[ix])
                ix += 1
            else:
                if data[ix] != 0xff:
                    kw = pp.code2kw[data[ix]]
                    ix += 1
                else:
                    kw = pp.code2kw[0xff00 + data[ix + 1]]
                    ix += 2
                if lastid and kw[0].isalnum():
                    line += " "
                lastid = False
                line += kw
        ix += 1
        pp.parse_line(line)
        listing += line + '\n'

    return pp, listing
