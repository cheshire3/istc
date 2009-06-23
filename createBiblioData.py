from lxml import etree

datafile = "/home/cheshire/cheshire3/dbs/istc/newBiblioData.txt"
outputfile = "/home/cheshire/cheshire3/dbs/istc/refsData/refs.xml"


file = open(datafile, 'r')
lines = file.readlines()
file.close()
output = []

for l in lines:
    toks = l.split('\t')
    output.append('<record><code>%s</code><full>%s</full></record>' % (toks[0].replace('&', '&amp;').strip(), toks[1].replace('&', '&amp;').strip()))
    test = etree.fromstring('<refs>%s</refs>' % ''.join(output))
tree = etree.fromstring('<refs>%s</refs>' % ''.join(output))           
parsedXslt = etree.parse("/home/cheshire/cheshire3/dbs/istc/xsl/reindent.xsl")
txr = etree.XSLT(parsedXslt)

result = txr(tree)
resultfile = open(outputfile, 'w')

resultfile.write(etree.tostring(result))
resultfile.flush()
resultfile.close()