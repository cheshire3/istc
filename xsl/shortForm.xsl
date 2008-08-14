<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="">

	 <xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8"/>
	 <xsl:preserve-space elements="xsl:text"/>

	<xsl:template match="/">	
		<xsl:call-template name="istcNumber"/>
		<!-- <xsl:call-template name="008"/> 
		<xsl:call-template name="author"/>	
		<xsl:call-template name="title"/>
		<xsl:call-template name="imprint"/>
		<xsl:call-template name="format"/>
		<xsl:call-template name="notes"/>
		<xsl:call-template name="references"/>	
		<xsl:call-template name="locations"/>	-->			
	</xsl:template>
	

	<xsl:template name="istcNumber">
		<xsl:value-of select="//controlfield[@tag='001']"/>
  </xsl:template> 
	
	 


</xsl:stylesheet>