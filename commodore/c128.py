from commodore import base

keywords = base.keywords + [
    ("rgr", 0xCC),
    ("rclr", 0xCD),
    ("joy", 0xCF),
    ("rdot", 0xD0),
    ("dec", 0xD1),
    ("hex$", 0xD2),
    ("err$", 0xD3),
    ("instr", 0xD4),
    ("else", 0xD5),
    ("resume", 0xD6),
    ("trap", 0xD7),
    ("tron", 0xD8),
    ("troff", 0xD9),
    ("sound", 0xDA),
    ("vol", 0xDB),
    ("auto", 0xDC),
    ("pudef", 0xDD),
    ("graphic", 0xDE),
    ("paint", 0xDF),
]

