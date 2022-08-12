import sys

from coco.coco import secb, ecb, decb, cb, sdecb
from coco.dragon import basic as dragon
from coco.dragon import ddos
from coco.getoptions import keywords, remarks, isdragon, options
from coco.labels import gettgtlabs, validatelabs, renumber, cleanlabs
from coco.pack import pack
from coco.tokens import tokenize, detokenize
from coco.variables import IDError, getidtype, getids, reid

if __name__ == "__main__":
    sys.stderr.write("This is a library")
