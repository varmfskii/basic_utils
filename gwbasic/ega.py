from .basica import keywords

keywords = keywords + [
    ("PCOPY", 0xFEA5)
]

if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
