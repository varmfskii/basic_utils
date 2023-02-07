import sys

from msbasic.labels import gettgtlabs, validatelabs, renumber, cleanlabs
from msbasic.pack import pack, splitlines
from msbasic.tokens import tokenize, detokenize
from msbasic.variables import IDError, getidtype, getids, reid

if __name__ == "__main__":
    sys.stderr.write("This is a library")
