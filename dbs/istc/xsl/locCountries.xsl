<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="text" />
	
	<xsl:template match="/">
		<xsl:apply-templates />		
	</xsl:template>
	
	<xsl:template match="record">
		<xsl:apply-templates />		
	</xsl:template>

	<xsl:template match="datafield[@tag='852']">
		<xsl:value-of select="./@tag"/>
	</xsl:template>
	
	<xsl:template match="datafield[starts-with(@tag, '9')]">
		<xsl:if test="not(./@tag='959')">
		<xsl:value-of select="./@tag"/>
		</xsl:if>
	</xsl:template>
	

	
	<xsl:template match="*"/>
	
</xsl:stylesheet>