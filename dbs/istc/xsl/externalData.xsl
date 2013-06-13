<?xml version="1.1" encoding="utf-8"?>
 
 
 
 <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
 
 <xsl:output method="text" omit-xml-declaration="yes" encoding="ascii"/>
 	
 	<xsl:template match="/">		
 		<xsl:apply-templates />		
 	</xsl:template>
 	
 	<xsl:template match="string">
 		<xsl:apply-templates />	
 	</xsl:template>
 	
  <xsl:template match="*">
        <xsl:text>&lt;</xsl:text><xsl:value-of select="name()"/>
        <xsl:for-each select="@*">
			  <xsl:text> </xsl:text>
			  <xsl:value-of select="name()"/>
			  <xsl:text>="</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text>
        </xsl:for-each>
 <xsl:text>&gt;</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>&lt;/</xsl:text><xsl:value-of select="name()"/><xsl:text>&gt;</xsl:text>
  </xsl:template> 


 
 </xsl:stylesheet>
 	
 