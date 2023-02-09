def tokenize_line(line, pp, be=True):
    # convert a parsed line into the tokenized format for a BASIC file
    tokens = []
    for (c, w) in line:
        if c == pp.LABEL:  # line number
            val = int(w)
            if be:
                tokens += [val // 256, val & 0xff]
            else:
                tokens += [val & 0xff, val // 256]

        elif c in [pp.QUOTED, pp.REMARK, pp.DATA]:
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


def detokenize_body(data, pp, be=True):
    listing = ""
    ix = 0

    while data[ix] != 0x00 or data[ix + 1] != 0x00:
        if be:
            line = f'{data[ix + 2] * 0x100 + data[ix + 3]} '
        else:
            line = f'{data[ix + 2] + data[ix + 3] * 0x100} '

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
