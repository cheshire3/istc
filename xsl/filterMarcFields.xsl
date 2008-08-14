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
  
  	<xsl:template match="leader">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
  	<xsl:template match="controlfield[@tag='001']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
 
  	<xsl:template match="controlfield[@tag='008']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
  	<xsl:template match="datafield[@tag='100']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='130']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='245']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='260'][1]">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='300']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='500']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='510']">
  		<xsl:copy-of select="."/>
  	</xsl:template>
  
    <xsl:template match="datafield[@tag='951']">
     	<xsl:choose>
     	<!-- 	<xsl:when test="contains(subfield[@code='a']/text(), 'Cambridge') and contains(subfield[@code='a']/text(), 'UL')"> -->
     		<xsl:when test="contains(subfield[@code='a']/text(), 'JRL')">
     			<xsl:copy-of select="."/>
     		</xsl:when>
     		<xsl:otherwise/>
     	</xsl:choose>
  		
  	</xsl:template>

	<xsl:template match="*"/>
 	
  
</xsl:stylesheet>