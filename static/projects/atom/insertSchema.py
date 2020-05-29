import xml.sax
from xml.sax.saxutils import XMLFilterBase, XMLGenerator

# All hail the monkey patch!
#
# https://sourceforge.net/tracker/?func=detail&atid=106473&aid=814935&group_id=6473
def resolveEntity(self, publicId, systemId):
    return self._ent_handler.resolveEntity(publicId, systemId)

XMLFilterBase.resolveEntity = resolveEntity

class ArtworkFilter(XMLFilterBase):
    def __init__(self, upstream, downstream, artDict):
        XMLFilterBase.__init__(self, upstream)
        self._downstream = downstream
        self._artDict = artDict
        return

    def startDocument(self):
        self._currentKey = None
        return

    def processingInstruction(self, target, body):
        self._downstream.processingInstruction(target, body)
        return

    def comment(self, body):
        self._downstream.comment(body)
        return

    def ignorableWhitespace(self, ws):
        self._downstream.ignorableWhitespace(ws)
        return

    def startElement(self, name, attrs):
        artName = attrs.get('name')
        self._downstream.startElement(name, attrs)
        if name=='artwork' and artName:
            #print "artName %s" % artName
            self._currentKey = artName
            if self._artDict.has_key(artName):
                self._downstream.characters("\n"+self._artDict[artName])
        return

    def endElement(self, name):
        if name=='artwork': self._currentKey=None
        self._downstream.endElement(name)
        return

    def characters(self, content):
        #Only forward the event if the state warrants it
        if not self._currentKey:
            self._downstream.characters(content)
        return

def stripSchematronAssertions(s):
    pattern = s.find("pattern")
    eqSign = s.find("=")+1
    start = s.find("[")
    end = s.rfind("]")+1
    if start>-1 and end > -1 and pattern < 0:
        return (s[0:eqSign] + s[end:]).strip()
    else:
        return s.strip()

def decomposeSchema(path, prefix):
    atomNamespace = None
    atomStart = None
    keys = []
    values = []

    schemaFile = open(path,"r")
    for line in schemaFile:
        if atomNamespace and atomStart:
            if line.startswith('#'):
                keys.append(line[line.find(" "):].strip())
                values.append("")
            elif len(values) > 0:
                values[-1]+=(line)
        elif line.startswith('start ='):
            # print line
            atomStart = line
        elif line.startswith('namespace'):
            # print line
            atomNamespace = line
    schemaFile.close()
    values = map(stripSchematronAssertions, values)
    results = dict(map(None, keys, values))
    results[prefix + "Start"] = atomStart
    results[prefix + "NS"] = atomNamespace
    return results



# Decompose the schema and insert it into the XML
allSchema = "./app.rnc"
catSchema = "./cat.rnc"
fragments = {}

if __name__ == "__main__":

    fragments.update(decomposeSchema(allSchema,"collection"))

    maxExampleFile = open("introspection.xml","r")
    fragments["introspectionDoc"] = maxExampleFile.read()
    maxExampleFile.close()

    allSchemaFile = open(allSchema,"r")
    fragments["app:allSchema"] = allSchemaFile.read()
    allSchemaFile.close()

    catSchemaFile = open(catSchema,"r")
    fragments["app:catSchema"] = catSchemaFile.read()
    catSchemaFile.close()

    parser = xml.sax.make_parser()

    import sys,codecs
    #XMLGenerator is a special SAX handler that merely writes
    #SAX events back into an XML document
    outputFile = codecs.open(sys.argv[2],"w","utf-8")
    outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    downstream_handler = XMLGenerator(outputFile)
    #upstream, the parser, downstream, the next handler in the chain
    filter_handler = ArtworkFilter(parser, downstream_handler, fragments)

    #The SAX filter base is designed so that the filter takes
    #on much of the interface of the parser itself, including the
    #"parse" method
    #print sys.argv[1]

    filter_handler.parse(file(sys.argv[1], "rb"))
    outputFile.close()









