<?xml version="1.0" ?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	
  <xsl:output method="xml" version="1.0" encoding="ascii"/>
  <xsl:preserve-space elements="xsl:text"/>
  
  <xsl:template match="/">
  		<xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="record">
  		<xsl:apply-templates />
  	</xsl:template>
  
  <xsl:template match="leader"/>
  
  <xsl:template match="controlfield">
  	<span><xsl:value-of select="@tag"/><xsl:text> </xsl:text><xsl:value-of select="."/></span><br/>
  </xsl:template>
  
  <xsl:template match="datafield">
  	<span><xsl:value-of select="@tag"/><xsl:text> </xsl:text><xsl:value-of select="@ind1"/><xsl:value-of select="@ind2"/>
  	<xsl:apply-templates select="subfield"/></span><br/>
  </xsl:template>
  
  <xsl:template match="subfield">
  	<xsl:text> $</xsl:text><xsl:value-of select="@code"/><xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:template>
  
  <xsl:template match="*"/>
  
</xsl:stylesheet>