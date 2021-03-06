<?xml version="1.0" ?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	
  <xsl:output method="text" version="1.0" encoding="utf-8"/>
  <xsl:preserve-space elements="xsl:text"/>
  
  <xsl:param name="newline">
  <xsl:text>
</xsl:text>
  </xsl:param>
  
  <xsl:template match="/">
  		<xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="record">
  		<xsl:apply-templates />
  	</xsl:template>
  
  <xsl:template match="leader"/>
  
  <xsl:template match="controlfield">
  	<xsl:value-of select="$newline"/><xsl:value-of select="@tag"/><xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:template>
  
  <xsl:template match="datafield">
  	<xsl:value-of select="$newline"/><xsl:value-of select="@tag"/><xsl:text> </xsl:text><xsl:value-of select="@ind1"/><xsl:value-of select="@ind2"/>
  	<xsl:apply-templates select="subfield"/>
  </xsl:template>
  
  <xsl:template match="subfield">
  	<xsl:text> $</xsl:text><xsl:value-of select="@code"/><xsl:text> </xsl:text><xsl:value-of select="."/>
  </xsl:template>
  
  <xsl:template match="*"/>
  
</xsl:stylesheet>