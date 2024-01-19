from msbasic.dialect import Dialect

color_keywords = [
    ("'", 0x3A83), ("*", 0xAD), ("+", 0xAB), ("-", 0xAC), ("/", 0xAE),
    ("<", 0xB4), ("=", 0xB3), (">", 0xB2), ("ABS", 0xFF82), ("AND", 0xB0),
    ("ASC", 0xFF8A), ("AUDIO", 0xA1), ("CHR$", 0xFF8B), ("CLEAR", 0x95),
    ("CLOAD", 0x97), ("CLOADM", 0x974d), ("CLOSE", 0x9A), ("CLS", 0x9E),
    ("CONT", 0x93), ("CSAVE", 0x98), ("CSAVEM", 0x984d), ("DATA", 0x86),
    ("DIM", 0x8C), ("ELSE", 0x3A84), ("END", 0x8A), ("EOF", 0xFF8C),
    ("EXEC", 0xA2), ("FOR", 0x80), ("GO", 0x81), ("GOSUB", 0x81A6),
    ("GOTO", 0x81A5), ("IF", 0x85), ("INKEY$", 0xFF92), ("INPUT", 0x89),
    ("INT", 0xFF81), ("JOYSTK", 0xFF8D), ("LEFT$", 0xFF8E), ("LEN", 0xFF87),
    ("LIST", 0x94), ("LLIST", 0x9B), ("MEM", 0xFF93), ("MID$", 0xFF90),
    ("MOTOR", 0x9F), ("NEW", 0x96), ("NEXT", 0x8B), ("NOT", 0xA8),
    ("OFF", 0xAA), ("ON", 0x88), ("OPEN", 0x99), ("OR", 0xB1),
    ("PEEK", 0xFF86), ("POINT", 0xFF91), ("POKE", 0x92), ("PRINT", 0x87),
    ("READ", 0x8D), ("REM", 0x82), ("RESET", 0x9D), ("RESTORE", 0x8F),
    ("RETURN", 0x90), ("RIGHT$", 0xFF8F), ("RND", 0xFF84), ("RUN", 0x8E),
    ("SET", 0x9C), ("SGN", 0xFF80), ("SIN", 0xFF85), ("SKIPF", 0xA3),
    ("SOUND", 0xA0), ("STEP", 0xA9), ("STOP", 0x91), ("STR$", 0xFF88),
    ("SUB", 0xA6), ("TAB(", 0xA4), ("THEN", 0xA7), ("TO", 0xA5),
    ("USR", 0xFF83), ("VAL", 0xFF89), ("^", 0xAF)
]


class CB(Dialect):
    id = 'Color BASIC'
    keywords = color_keywords
    dragon = False
    disk = False


extended_keywords = [
    ("ATN", 0xFF94), ("CIRCLE", 0xC2), ("COLOR", 0xC1), ("COS", 0xFF95),
    ("DEF", 0xB9), ("DEL", 0xB5), ("DLOAD", 0xCA), ("DLOADM", 0xca4d),
    ("DRAW", 0xC6), ("EDIT", 0xB6), ("EXP", 0xFF97), ("FIX", 0xFF98),
    ("FN", 0xCC), ("GET", 0xC4), ("HEX$", 0xFF9C), ("INSTR", 0xFF9E),
    ("LET", 0xBA), ("LINE", 0xBB), ("LOG", 0xFF99), ("PAINT", 0xC3),
    ("PCLEAR", 0xC0), ("PCLS", 0xBC), ("PCOPY", 0xC7), ("PLAY", 0xC9),
    ("PMODE", 0xC8), ("POS", 0xFF9A), ("PPOINT", 0xFFA0), ("PRESET", 0xBE),
    ("PSET", 0xBD), ("PUT", 0xC5), ("RENUM", 0xCB), ("SCREEN", 0xBF),
    ("SQR", 0xFF9B), ("STRING$", 0xFFA1), ("TAN", 0xFF96), ("TIMER", 0xFF9F),
    ("TROFF", 0xB8), ("TRON", 0xB7), ("USING", 0xCD), ("VARPTR", 0xFF9D)
]

extended_preserve = ['B', 'BF', 'G']


class ECB(Dialect):
    id = 'Extended Color BASIC'
    keywords = color_keywords + extended_keywords
    dragon = False
    preserve = extended_preserve


disk_keywords = [
    ("AS", 0xFFA7), ("BACKUP", 0xDD), ("COPY", 0xDE), ("CVN", 0xFFA2),
    ("DIR", 0xCE), ("DOS", 0xE1), ("DRIVE", 0xCF), ("DSKI$", 0xDF),
    ("DSKINI", 0xDC), ("DSKO$", 0xE0), ("FIELD", 0xD0), ("FILES", 0xD1),
    ("FREE", 0xFFA3), ("KILL", 0xD2), ("LOAD", 0xD3), ("LOADM", 0xd34d),
    ("LOC", 0xFFA4), ("LOF", 0xFFA5), ("LSET", 0xD4), ("MERGE", 0xD5),
    ("MKN$", 0xFFA6), ("RENAME", 0xD6), ("RSET", 0xD7), ("SAVE", 0xD8),
    ("SAVEM", 0xd84d), ("UNLOAD", 0xDB), ("VERIFY", 0xDA), ("WRITE", 0xD9)
]

disk_preserve = ['A', 'R']


class DECB(Dialect):
    id = 'Disk Extended Color Basic'
    keywords = color_keywords + extended_keywords + disk_keywords
    dragon = False
    disk = True
    preserve = disk_preserve + extended_preserve


super_keywords = [
    ("ATTR", 0xF8), ("BRK", 0xF0), ("BUTTON", 0xFFA9), ("CMP", 0xF6),
    ("ERLIN", 0xFFAC), ("ERNO", 0xFFAB), ("ERR", 0xEF), ("HBUFF", 0xED),
    ("HCIRCLE", 0xE9), ("HCLS", 0xE6), ("HCOLOR", 0xE7), ("HDRAW", 0xF5),
    ("HGET", 0xEB), ("HLINE", 0xEA), ("HPAINT", 0xE8), ("HPOINT", 0xFFAA),
    ("HPRINT", 0xEE), ("HPUT", 0xEC), ("HRESET", 0xF4), ("HSCREEN", 0xE4),
    ("HSET", 0xF3), ("HSTAT", 0xF2), ("LOCATE", 0xF1), ("LPEEK", 0xFFA8),
    ("LPOKE", 0xE5), ("PALETTE", 0xE3), ("RGB", 0xF7), ("WIDTH", 0xE2)
]


class SECB(Dialect):
    id = 'Extended Color BASIC (CoCo 3)'
    keywords = color_keywords + extended_keywords + super_keywords
    dragon = False
    disk = False
    preserve = extended_preserve


class SDECB(Dialect):
    id = 'Disk Extended Color (CoCo 3)'
    keywords = color_keywords + extended_keywords + super_keywords + disk_keywords
    dragon = False
    disk = True
    preserve = disk_preserve + extended_preserve


dragon_keywords = [
    ("'", 0x3A83), ("*", 0xC5), ("+", 0xC3), ("-", 0xC4), ("/", 0xC6),
    ("<", 0xCC), ("=", 0xCB), (">", 0xCA), ("ABS", 0xFF82), ("AND", 0xC8),
    ("ASC", 0xFF90), ("ATN", 0xFF8B), ("AUDIO", 0xA3), ("CHR$", 0xFF91),
    ("CIRCLE", 0xB1), ("CLEAR", 0x96), ("CLOAD", 0x99), ("CLOSE", 0x9C),
    ("CLS", 0xA0), ("COLOR", 0xB0), ("CONT", 0x94), ("COS", 0xFF89),
    ("CSAVE", 0x9A), ("DATA", 0x86), ("DEF", 0x98), ("DEL", 0xA6),
    ("DIM", 0x8C), ("DLOAD", 0xB9), ("DRAW", 0xB5), ("EDIT", 0xA7),
    ("ELSE", 0x3A84), ("END", 0x8A), ("EOF", 0xFF92), ("EXEC", 0xA4),
    ("EXP", 0xFF87), ("FIX", 0xFF94), ("FN", 0xBE), ("FOR", 0x80),
    ("GET", 0xB3), ("GO", 0x81), ("GOSUB", 0x81BD), ("GOTO", 0x81BC),
    ("HEX$", 0xFF95), ("IF", 0x85), ("INKEY$", 0xFF9A), ("INPUT", 0x89),
    ("INSTR", 0xFF9D), ("INT", 0xFF81), ("JOYSTK", 0xFF93), ("LEFT$", 0xFF96),
    ("LEN", 0xFF8D), ("LET", 0x8E), ("LINE", 0xAA), ("LIST", 0x95),
    ("LLIST", 0x9D), ("LOG", 0xFF86), ("MEM", 0xFF9B), ("MID$", 0xFF98),
    ("MOTOR", 0xA1), ("NEW", 0x97), ("NEXT", 0x8B), ("NOT", 0xC0),
    ("OFF", 0xC2), ("ON", 0x88), ("OPEN", 0x9B), ("OR", 0xC9), ("PAINT", 0xB2),
    ("PCLEAR", 0xAF), ("PCLS", 0xAB), ("PCOPY", 0xB6), ("PEEK", 0xFF8C),
    ("PLAY", 0xB8), ("PMODE", 0xB7), ("POINT", 0xFF99), ("POKE", 0x93),
    ("POS", 0xFF83), ("PPOINT", 0xFF9F), ("PRESET", 0xAD), ("PRINT", 0x87),
    ("PSET", 0xAC), ("PUT", 0xB4), ("READ", 0x8D), ("REM", 0x82),
    ("RENUM", 0xBA), ("RESET", 0x9F), ("RESTORE", 0x90), ("RETURN", 0x91),
    ("RIGHT$", 0xFF97), ("RND", 0xFF84), ("RUN", 0x8F), ("SCREEN", 0xAE),
    ("SET", 0x9E), ("SGN", 0xFF80), ("SIN", 0xFF88), ("SKIPF", 0xA5),
    ("SOUND", 0xA2), ("SQR", 0xFF85), ("STEP", 0xC1), ("STOP", 0x92),
    ("STR$", 0xFF8E), ("STRING$", 0xFFA0), ("SUB", 0xBD), ("TAB(", 0xBB),
    ("TAN", 0xFF8A), ("THEN", 0xBF), ("TIMER", 0xFF9E), ("TO", 0xBC),
    ("TROFF", 0xA9), ("TRON", 0xA8), ("USING", 0xCD), ("USR", 0xFFA1),
    ("VAL", 0xFF8F), ("VARPTR", 0xFF9C), ("^", 0xC7)
]

dragon_preserve = ['B', 'BF', 'G']


class Dragon(Dialect):
    id = 'Dragon BASIC'
    keywords = dragon_keywords
    dragon = True
    disk = False
    preserve = dragon_preserve


ddos_keywords = [
    ("AUTO", 0xCE), ("BACKUP", 0xCF), ("BEEP", 0xD0), ("BOOT", 0xD1),
    ("CHAIN", 0xD2), ("COPY", 0xD3), ("CREATE", 0xD4), ("DIR", 0xD5),
    ("DRIVE", 0xD6), ("DSKINIT", 0xD7), ("ERL", 0xFFA4), ("ERR", 0xFFA5),
    ("ERROR", 0xDA), ("FLREAD", 0xE6), ("FRE$", 0xFFA8), ("FREAD", 0xD8),
    ("FREE", 0xFFA3), ("FROM", 0xE5), ("FWRITE", 0xD9), ("HIMEM", 0xFFA6),
    ("KILL", 0xDB), ("LOAD", 0xDC), ("LOC", 0xFFA7), ("LOF", 0xFFA2),
    ("MERGE", 0xDD), ("PROTECT", 0xDE), ("RENAME", 0xE0), ("SAVE", 0xE1),
    ("SREAD", 0xE2), ("SWAP", 0xE7), ("SWRITE", 0xE3), ("VERIFY", 0xE4),
    ("WAIT", 0xDF)
]

ddos_preserve = ['A', 'R']


class DDOS(Dialect):
    id = 'Dragon DOS'
    keywords = dragon_keywords + ddos_keywords
    dragon = True
    disk = True
    preserve = ddos_preserve + dragon_preserve


DIALECTS = {
    'cb': CB, 'ecb': ECB, 'decb': DECB, 'secb': SECB, 'sdecb': SDECB,
    'dragon': Dragon, 'ddos': DDOS
}
