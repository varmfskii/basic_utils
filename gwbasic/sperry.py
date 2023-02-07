from .basica import keywords

keywords = keywords + [
    ("DEBUG", 0xFEA4),
]

if __name__ == "__main__":
    import sys

    sys.stderr.write("This is a library")
