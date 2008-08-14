<?xml version="1.1" encoding="utf-8"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:template match="/">
		<h1><xsl:value-of select="$a"/></h1>
		<h2><xsl:value-of select="$b"/></h2>
		<h3><xsl:value-of select="$temp"/></h3>
	</xsl:template>
	

</xsl:stylesheet>