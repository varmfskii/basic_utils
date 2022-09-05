from .color import color_keywords
from .disk import disk_keywords
from .extended import ext_keywords
from .cb import special

keywords = color_keywords + ext_keywords + disk_keywords
special += ["LOAD", "SAVE"]

