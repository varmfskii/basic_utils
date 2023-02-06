keywords = [
    ("END", 0x80),
    ("FOR", 0x81),
    ("NEXT", 0x82),
    ("DATA", 0x83),
    ("INPUT", 0x84),
    ("DEL", 0x85),
    ("DIM", 0x86),
    ("READ", 0x87),
    ("GR", 0x88),
    ("TEXT", 0x89),
    ("PR #", 0x8A),
    ("IN #", 0x8B),
    ("CALL", 0x8C),
    ("PLOT", 0x8D),
    ("HLIN", 0x8E),
    ("VLIN", 0x8F),
    ("HGR2", 0x90),
    ("HGR", 0x91),
    ("HCOLOR=", 0x92),
    ("HPLOT", 0x93),
    ("DRAW", 0x94),
    ("XDRAW", 0x95),
    ("HTAB", 0x96),
    ("HOME", 0x97),
    ("ROT=", 0x98),
    ("SCALE=", 0x99),
    ("SHLOAD", 0x9A),
    ("TRACE", 0x9B),
    ("NOTRACE", 0x9C),
    ("NORMAL", 0x9D),
    ("INVERSE", 0x9E),
    ("FLASH", 0x9F),
    ("COLOR=", 0xA0),
    ("POP", 0xA1),
    ("VTAB", 0xA2),
    ("HIMEM:", 0xA3),
    ("LOMEM:", 0xA4),
    ("ONERR", 0xA5),
    ("RESUME", 0xA6),
    ("RECALL", 0xA7),
    ("STORE", 0xA8),
    ("SPEED=", 0xA9),
    ("LET", 0xAA),
    ("GOTO", 0xAB),
    ("RUN", 0xAC),
    ("IF", 0xAD),
    ("RESTORE", 0xAE),
    ("&", 0xAF),
    ("GOSUB", 0xB0),
    ("RETURN", 0xB1),
    ("REM", 0xB2),
    ("STOP", 0xB3),
    ("ON", 0xB4),
    ("WAIT", 0xB5),
    ("LOAD", 0xB6),
    ("SAVE", 0xB7),
    ("DEF FN", 0xB8),
    ("POKE", 0xB9),
    ("PRINT", 0xBA),
    ("CONT", 0xBB),
    ("LIST", 0xBC),
    ("CLEAR", 0xBD),
    ("GET", 0xBE),
    ("NEW", 0xBF),
    ("TAB", 0xC0),
    ("TO", 0xC1),
    ("FN", 0xC2),
    ("SPC(", 0xC3),
    ("THEN", 0xC4),
    ("AT", 0xC5),
    ("NOT", 0xC6),
    ("STEP", 0xC7),
    ("+", 0xC8),
    ("-", 0xC9),
    ("*", 0xCA),
    ("/", 0xCB),
    (";", 0xCC),
    ("AND", 0xCD),
    ("OR", 0xCE),
    (">", 0xCF),
    ("=", 0xD0),
    ("<", 0xD1),
    ("SGN", 0xD2),
    ("INT", 0xD3),
    ("ABS", 0xD4),
    ("USR", 0xD5),
    ("FRE", 0xD6),
    ("SCRN (", 0xD7),
    ("PDL", 0xD8),
    ("POS", 0xD9),
    ("SQR", 0xDA),
    ("RND", 0xDB),
    ("LOG", 0xDC),
    ("EXP", 0xDD),
    ("COS", 0xDE),
    ("SIN", 0xDF),
    ("TAN", 0xE0),
    ("ATN", 0xE1),
    ("PEEK", 0xE2),
    ("LEN", 0xE3),
    ("STR$", 0xE4),
    ("VAL", 0xE5),
    ("ASC", 0xE6),
    ("CHR$", 0xE7),
    ("LEFT$", 0xE8),
    ("RIGHT$", 0xE9),
    ("MID$", 0xEA)
]

remarks = ["REM"]

if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
