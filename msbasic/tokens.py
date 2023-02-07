from basic69.coco import sdecb
from basic69.dragon import ddos
from basic69 import Parser


def tokenize_line(line):
    # convert a parsed line into the tokenized format for a BASIC file
    tokens = []
    for (c, w) in line:
        if c == Parser.LABEL:  # line number
            val = int(w)
            tokens += [val // 256, val & 0xff]
        elif c in [Parser.QUOTED, Parser.REMARK, Parser.DATA]:
            # explicit text
            for char in w:
                tokens.append(ord(char))
        elif c < 0x80 or 0x100 <= c < 0x200:
            # code text, interpreter only recognizes uppercase
            for char in w.upper():
                tokens.append(ord(char))
        elif c < 0x100:  # tokenized keyword
            tokens.append(c)
        elif c < 0x10000:  # tokenized extended keyword
            tokens += [c // 256, c & 0xff]
        else:  # three byte keyword (not coco or dragon)
            tokens += [c // 0x10000, (c // 0x100) & 0xff, c & 0xff]
    tokens.append(0)
    return tokens


def tokenize(pp, ws=False):
    # convert a parsed file into tokenized BASIC file
    if ws:
        parsed = pp.full_parse
    else:
        parsed = pp.no_ws()
    tokenized = []
    address = pp.address
    for line in parsed:
        line_tokens = tokenize_line(line)
        address += 2 + len(line_tokens)
        tokenized += [address // 0x100, address & 0xff] + line_tokens
    tokenized += [0, 0]
    if pp.isdragon:
        val = len(tokenized)
        tokenized = [0x55, 0x01, 0x24, 0x01, val // 256, val & 0xff, 0x8b, 0x8d, 0xaa] + tokenized
    elif pp.disk:
        val = len(tokenized)
        tokenized = [0xff, val // 0x100, val & 0xff] + tokenized
    return bytearray(tokenized)


def detokenize(opts, data):
    data = list(data)
    listing = ""

    if data[0] == 0x55:
        ix = 9
        opts.keywords, opts.remarks = ddos.keywords, ddos.remarks
        pp = Parser(opts)
    elif data[0] == 0xff:
        ix = 3
        opts.keywords, opts.remarks = sdecb.keywords, sdecb.remarks
    else:
        ix = 0
        opts.keywords, opts.remarks = sdecb.keywords, sdecb.remarks
    pp = Parser(opts)

    while data[ix] != 0x00 or data[ix + 1] != 0x00:
        line = f'{data[ix + 2] * 0x100 + data[ix + 3]} '
        ix += 4
        lastid = False
        while data[ix] != 0x00:
            c1 = data[ix]
            ix = ix + 1
            c2 = data[ix]
            if c1 * 0x100 + c2 in pp.code2kw.keys():
                kw = pp.code2kw[c1 * 0x100 + c2]
                ix += 1
                iskw = True
            elif c1 in pp.code2kw.keys():
                kw = pp.code2kw[c1]
                iskw = True
            else:
                kw = chr(c1)
                iskw = False
                if kw.isalpha():
                    # A-Z
                    lastid = True
                elif not kw.isdigit():
                    # not 0-9
                    lastid = False
            if iskw:
                if lastid and kw[0].isalpha():
                    line += ' '
                lastid = False
            line += kw

        ix += 1
        pp.parse_txt(line)
        listing += line + '\n'

    return pp, listing
