
#Used to clean create new USA location data when moving from C2 to C3 (June 2009)


from lxml import etree

datafile = "/home/cheshire/cheshire3/dbs/istc/dataCleaning/newUsaData.txt"
outputfile = "/home/cheshire/cheshire3/dbs/istc/usaData/usaCodes.xml"


file = open(datafile, 'r')
lines = file.readlines()
file.close()
output = []

for l in lines:
    toks = l.split('\t')
    output.append('<record><code>%s</code><full>%s</full></record>' % (toks[0], toks[1].replace('&', '&amp;').strip()))

tree = etree.fromstring('<usa>%s</usa>' % ''.join(output))           
parsedXslt = etree.parse("/home/cheshire/cheshire3/dbs/istc/xsl/reindent.xsl")
txr = etree.XSLT(parsedXslt)

result = txr(tree)
resultfile = open(outputfile, 'w')

resultfile.write(etree.tostring(result))
resultfile.flush()
resultfile.close()
                  