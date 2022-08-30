INSTDIR ?= /usr/local
LIBS = coco_dragon parser
BINS = coco_detokenize.py coco_pack.py coco_reid.py coco_renumber.py	\
	coco_tokenize.py coco_unpack.py

install:
	cp -R ${LIBS} ${INSTDIR}/python
	cp ${BINS} ${INSTDIR}/bin

.PHONY: install clean

clean:
	find . -name "*~" -delete

