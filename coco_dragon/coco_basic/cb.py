from .color import color_keywords
from parser import Types
import re

keywords = color_keywords
special = ["REM", "'", "CLOAD", "CSAVE"]


def do_special(parent, code, parsed, line):
    if code in [parent.kw2code["REM"], parent.kw2code["'"]]:
        if parent.pos != parent.line_len:
            parsed.append((Types.OTHER, line[parent.pos:]))
            parent.pos = parent.line_len
    else:
        match = re.match('^( +[Mm])')
        if match:
            parsed.append((Types.OTHER, match[0]))
            parent.pos += len(match[0])
