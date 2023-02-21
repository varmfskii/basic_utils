from . import dragon

keywords = dragon.keywords + [
    ("AUTO", 0xCE),
    ("BACKUP", 0xCF),
    ("BEEP", 0xD0),
    ("BOOT", 0xD1),
    ("CHAIN", 0xD2),
    ("COPY", 0xD3),
    ("CREATE", 0xD4),
    ("DIR", 0xD5),
    ("DRIVE", 0xD6),
    ("DSKINIT", 0xD7),
    ("ERL", 0xFFA4),
    ("ERR", 0xFFA5),
    ("ERROR", 0xDA),
    ("FLREAD", 0xE6),
    ("FRE$", 0xFFA8),
    ("FREAD", 0xD8),
    ("FREE", 0xFFA3),
    ("FROM", 0xE5),
    ("FWRITE", 0xD9),
    ("HIMEM", 0xFFA6),
    ("KILL", 0xDB),
    ("LOAD", 0xDC),
    ("LOC", 0xFFA7),
    ("LOF", 0xFFA2),
    ("MERGE", 0xDD),
    ("PROTECT", 0xDE),
    ("RENAME", 0xE0),
    ("SAVE", 0xE1),
    ("SREAD", 0xE2),
    ("SWAP", 0xE7),
    ("SWRITE", 0xE3),
    ("VERIFY", 0xE4),
    ("WAIT", 0xDF)
]

remarks = dragon.remarks
specials = dragon.specials
