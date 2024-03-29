LIBS = basic69 msbasic
BINS = coco.py

PYTHONLIB=$(shell printf "import sys\nfor dir in sys.path:\n\tprint(dir)\n"|python3|grep -v '\.zip$'|grep '.'|head -1)

ifdef INSTDIR
LIBDIR=${INSTDIR}/python
BINDIR=${INSTDIR}/bin
else
LIBDIR=${PYTHONLIB}
BINDIR=/usr/local/bin
endif

install:
	cp -R ${LIBS} ${INSTDIR}/python
	cp ${BINS} ${INSTDIR}/bin

.PHONY: install clean

clean:
	find . -name "*~" -delete

