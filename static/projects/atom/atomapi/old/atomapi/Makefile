NAME=draft-ietf-atompub-protocol
REV=03
LASTREV=02
LAST=$(NAME)-$(LASTREV)
SOURCE=$(NAME)
TARGET=$(NAME)-$(REV)

default: $(TARGET).html $(TARGET).txt diff nits

$(TARGET).html: $(SOURCE).xml rfc2629.xslt
	xsltproc rfc2629.xslt $(SOURCE).xml > $(TARGET).html

$(TARGET).txt:  $(SOURCE).xml xml2rfc.tcl
	tclsh xml2rfc.tcl xml2rfc $(SOURCE).xml $(TARGET).txt

.PHONY: diff
diff:
	./rfcdiff.sh --html $(LAST).txt $(TARGET).txt

.PHONY: nits
nits:
	./idnits --verbose $(TARGET).txt

