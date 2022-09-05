import sys

from coco_dragon.coco_basic import secb, ecb, decb, cb, sdecb
from coco_dragon.dragon_basic import basic as dragon
from coco_dragon.dragon_basic import ddos
from coco_dragon.getoptions import dialect, options
from coco_dragon.labels import gettgtlabs, validatelabs, renumber, cleanlabs
from coco_dragon.pack import pack, splitlines
from coco_dragon.tokens import tokenize, detokenize
from coco_dragon.variables import IDError, getidtype, getids, reid

if __name__ == "__main__":
    sys.stderr.write("This is a library")
