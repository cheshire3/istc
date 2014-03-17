<?xml version="1.0" ?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	
  <xsl:output method="xml" version="1.0"/>
	<xsl:strip-space elements="*"/>


  <xsl:template match="/">
  		<xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="record">
  	<record>
  		<xsl:apply-templates />
  		</record>
  	</xsl:template>
    
    <xsl:template match="datafield[starts-with(@tag, '9')][subfield[@code='x']]"/>  	
     	
	<xsl:template match="*">
		<xsl:copy-of select="."/>
	</xsl:template>
 	
  
</xsl:stylesheet>