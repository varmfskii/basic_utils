keywords = [
    ("END", 0x81),
    ("FOR", 0x82),
    ("NEXT", 0x83),
    ("DATA", 0x84),
    ("INPUT", 0x85),
    ("DIM", 0x86),
    ("READ", 0x87),
    ("LET", 0x88),
    ("GOTO", 0x89),
    ("RUN", 0x8A),
    ("IF", 0x8B),
    ("RESTORE", 0x8C),
    ("GOSUB", 0x8D),
    ("RETURN", 0x8E),
    ("REM", 0x8F),
    ("STOP", 0x90),
    ("PRINT", 0x91),
    ("CLEAR", 0x92),
    ("LIST", 0x93),
    ("NEW", 0x94),
    ("ON", 0x95),
    ("DEF", 0x96),
    ("POKE", 0x97),
    ("CONT", 0x98),
    ("LPRINT", 0x9B),
    ("LLIST", 0x9C),
    ("WIDTH", 0x9D),
    ("ELSE", 0x9E),
    ("TRACE", 0x9F),
    ("NOTRACE", 0xA0),
    ("SWAP", 0xA1),
    ("ERASE", 0xA2),
    ("EDIT", 0xA3),
    ("ERROR", 0xA4),
    ("RESUME", 0xA5),
    ("DEL", 0xA6),
    ("AUTO", 0xA7),
    ("RENUM", 0xA8),
    ("DEFSTR", 0xA9),
    ("DEFINT", 0xAA),
    ("DEFSNG", 0xAB),
    ("DEFDBL", 0xAC),
    ("LINE", 0xAD),
    ("POP", 0xAE),
    ("WHILE", 0xAF),
    ("WEND", 0xB0),
    ("CALL", 0xB1),
    ("WRITE", 0xB2),
    ("COMMON", 0xB3),
    ("CHAIN", 0xB4),
    ("OPTION", 0xB5),
    ("RANDOMIZE", 0xB6),
    ("SYSTEM", 0xB7),
    ("OPEN", 0xB8),
    ("FIELD", 0xB9),
    ("GET", 0xBA),
    ("PUT", 0xBB),
    ("CLOSE", 0xBC),
    ("LOAD", 0xBD),
    ("MERGE", 0xBE),
    ("FILES", 0xBF),
    ("NAME", 0xC0),
    ("KILL", 0xC1),
    ("LSET", 0xC2),
    ("RSET", 0xC3),
    ("SAVE", 0xC4),
    ("RESET", 0xC5),
    ("TEXT", 0xC6),
    ("HOME", 0xC7),
    ("VTAB", 0xC8),
    ("HTAB", 0xC9),
    ("INVERSE", 0xCA),
    ("NORMAL", 0xCB),
    ("GR", 0xCC),
    ("COLOR", 0xCD),
    ("HLIN", 0xCE),
    ("VLIN", 0xCF),
    ("PLOT", 0xD0),
    ("HGR", 0xD1),
    ("HPLOT", 0xD2),
    ("HCOLOR", 0xD3),
    ("BEEP", 0xD4),
    ("WAIT", 0xD5),
    ("TO", 0xDD),
    ("THEN", 0xDE),
    ("TAB(", 0xDF),
    ("STEP", 0xE0),
    ("USR", 0xE1),
    ("FN", 0xE2),
    ("SPC(", 0xE3),
    ("NOT", 0xE4),
    ("ERL", 0xE5),
    ("ERR", 0xE6),
    ("STRING$", 0xE7),
    ("USING", 0xE8),
    ("INSTR", 0xE9),
    ("'", 0xEA),
    ("VARPTR", 0xEB),
    ("SCRN", 0xEC),
    ("HSCRN", 0xED),
    ("INKEY$", 0xEE),
    (">", 0xEF),
    ("=", 0xE0),
    ("<", 0xF1),
    ("+", 0xF2),
    ("-", 0xF3),
    ("*", 0xF4),
    ("/", 0xF5),
    ("^", 0xF6),
    ("AND", 0xF7),
    ("OR", 0xF8),
    ("XOR", 0xF9),
    ("EQV", 0xFA),
    ("IMP", 0xFB),
    ("MOD", 0xFC),
    ("LEFT$", 0xFD81),
    ("RIGHT$", 0xFD82),
    ("MID$", 0xFD83),
    ("SGN", 0xFD84),
    ("INT", 0xFD85),
    ("SQR", 0xFD87),
    ("RND", 0xFD88),
    ("SIN", 0xFD89),
    ("LOG", 0xFD8A),
    ("EXP", 0xFD8B),
    ("COS", 0xFD8C),
    ("TAN", 0xFD8D),
    ("ATN", 0xFD8E),
    ("FRE", 0xFD8F),
    ("POS", 0xFD90),
    ("LEN", 0xFD91),
    ("STR$", 0xFD92),
    ("VAL", 0xFD93),
    ("ASC", 0xFD94),
    ("CHR$", 0xFD95),
    ("PEEK", 0xFD96),
    ("SPACE$", 0xFD97),
    ("OCT$", 0xFD98),
    ("HEX$", 0xFD99),
    ("LPOS", 0xFD9A),
    ("CINT", 0xFD9B),
    ("CSNG", 0xFD9C),
    ("CDBL", 0xFD9D),
    ("FIX", 0xFD9E),
    ("CVI", 0xFDAA),
    ("CVS", 0xFDAB),
    ("CVD", 0xFDAC),
    ("EOF", 0xFDAE),
    ("LOC", 0xFDAF),
    ("LOF", 0xFDB0),
    ("MKI$", 0xFDB1),
    ("MKS$", 0xFDB2),
    ("MKD$", 0xFDB3),
    ("VPOS", 0xFDB4),
    ("PDL", 0xFDB5),
    ("BUTTON", 0xFDB6)
]

remarks = ["REM", "'"]

if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
