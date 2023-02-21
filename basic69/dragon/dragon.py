keywords = [
    ("'", 0x3A83),
    ("*", 0xC5),
    ("+", 0xC3),
    ("-", 0xC4),
    ("/", 0xC6),
    ("<", 0xCC),
    ("=", 0xCB),
    (">", 0xCA),
    ("ABS", 0xFF82),
    ("AND", 0xC8),
    ("ASC", 0xFF90),
    ("ATN", 0xFF8B),
    ("AUDIO", 0xA3),
    ("CHR$", 0xFF91),
    ("CIRCLE", 0xB1),
    ("CLEAR", 0x96),
    ("CLOAD", 0x99),
    ("CLOSE", 0x9C),
    ("CLS", 0xA0),
    ("COLOR", 0xB0),
    ("CONT", 0x94),
    ("COS", 0xFF89),
    ("CSAVE", 0x9A),
    ("DATA", 0x86),
    ("DEF", 0x98),
    ("DEL", 0xA6),
    ("DIM", 0x8C),
    ("DLOAD", 0xB9),
    ("DRAW", 0xB5),
    ("EDIT", 0xA7),
    ("ELSE", 0x3A84),
    ("END", 0x8A),
    ("EOF", 0xFF92),
    ("EXEC", 0xA4),
    ("EXP", 0xFF87),
    ("FIX", 0xFF94),
    ("FN", 0xBE),
    ("FOR", 0x80),
    ("GET", 0xB3),
    ("GO", 0x81),
    ("GOSUB", 0x81BD),
    ("GOTO", 0x81BC),
    ("HEX$", 0xFF95),
    ("IF", 0x85),
    ("INKEY$", 0xFF9A),
    ("INPUT", 0x89),
    ("INSTR", 0xFF9D),
    ("INT", 0xFF81),
    ("JOYSTK", 0xFF93),
    ("LEFT$", 0xFF96),
    ("LEN", 0xFF8D),
    ("LET", 0x8E),
    ("LINE", 0xAA),
    ("LIST", 0x95),
    ("LLIST", 0x9D),
    ("LOG", 0xFF86),
    ("MEM", 0xFF9B),
    ("MID$", 0xFF98),
    ("MOTOR", 0xA1),
    ("NEW", 0x97),
    ("NEXT", 0x8B),
    ("NOT", 0xC0),
    ("OFF", 0xC2),
    ("ON", 0x88),
    ("OPEN", 0x9B),
    ("OR", 0xC9),
    ("PAINT", 0xB2),
    ("PCLEAR", 0xAF),
    ("PCLS", 0xAB),
    ("PCOPY", 0xB6),
    ("PEEK", 0xFF8C),
    ("PLAY", 0xB8),
    ("PMODE", 0xB7),
    ("POINT", 0xFF99),
    ("POKE", 0x93),
    ("POS", 0xFF83),
    ("PPOINT", 0xFF9F),
    ("PRESET", 0xAD),
    ("PRINT", 0x87),
    ("PSET", 0xAC),
    ("PUT", 0xB4),
    ("READ", 0x8D),
    ("REM", 0x82),
    ("RENUM", 0xBA),
    ("RESET", 0x9F),
    ("RESTORE", 0x90),
    ("RETURN", 0x91),
    ("RIGHT$", 0xFF97),
    ("RND", 0xFF84),
    ("RUN", 0x8F),
    ("SCREEN", 0xAE),
    ("SET", 0x9E),
    ("SGN", 0xFF80),
    ("SIN", 0xFF88),
    ("SKIPF", 0xA5),
    ("SOUND", 0xA2),
    ("SQR", 0xFF85),
    ("STEP", 0xC1),
    ("STOP", 0x92),
    ("STR$", 0xFF8E),
    ("STRING$", 0xFFA0),
    ("SUB", 0xBD),
    ("TAB(", 0xBB),
    ("TAN", 0xFF8A),
    ("THEN", 0xBF),
    ("TIMER", 0xFF9E),
    ("TO", 0xBC),
    ("TROFF", 0xA9),
    ("TRON", 0xA8),
    ("USING", 0xCD),
    ("USR", 0xFFA1),
    ("VAL", 0xFF8F),
    ("VARPTR", 0xFF9C),
    ("^", 0xC7)
]

remarks = ["REM", "'"]
specials = {
    'DATA': ['DATA'],
    'ELSE': ['ELSE'],
    'FOR': ['FOR'],
    'GO': ['GO'],
    'GOSUB': ['GOSUB'],
    'GOTO': ['GOTO'],
    'IF': ['IF'],
    'NEXT': ['NEXT'],
    'REM': ['REM', "'"],
    'SUB': ['SUB'],
    'THEN': ['THEN'],
    'TO': ['TO']
}