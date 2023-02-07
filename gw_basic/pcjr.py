from .basica import keywords

keywords = keywords + [
    ("NOISE", 0xFEA4),
    ("PCOPY", 0xFEA5),
    ("TERM", 0xFEA6)
]

if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
