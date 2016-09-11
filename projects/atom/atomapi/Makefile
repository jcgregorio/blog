NAME=draft-ietf-atompub-protocol
REV=17
LASTREV=16
LAST=$(NAME)-$(LASTREV)
SOURCE=$(NAME)
TARGET=$(NAME)-$(REV)

default: insertArt $(TARGET).html $(TARGET).txt diff nits

$(TARGET).html: $(SOURCE)-out.xml rfc2629.xslt
	xsltproc rfc2629.xslt $(SOURCE)-out.xml > $(TARGET).html

$(TARGET).txt:  $(SOURCE)-out.xml xml2rfc.tcl
	tclsh xml2rfc.tcl xml2rfc $(SOURCE)-out.xml $(TARGET).txt

.PHONY: insertArt
insertArt:
	python2.4 ./insertSchema.py $(SOURCE).xml $(SOURCE)-out.xml
	cp $(SOURCE)-out.xml $(SOURCE)-$(REV).xml

.PHONY: diff
diff:
	./rfcdiff.sh --html $(LAST).txt $(TARGET).txt
	#mv ./draft-ietf-atompub-protocol-17-from-6.diff.html ./draft-ietf-atompub-protocol-17-from-16.diff.html
.PHONY: nits
nits:
	./idnits --verbose $(TARGET).txt

