<?xml version="1.0" ?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	
  <xsl:output method="xml" version="1.0"/>
<xsl:strip-space elements="*"/>

	<xsl:param name="locfilter">
		<xsl:text>all</xsl:text>
	</xsl:param>

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
  	
  	<xsl:template match="controlfield[@tag='003']">
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
  
    <xsl:template match="datafield">  	
     	<xsl:if test="starts-with(@tag, '9') and not(subfield[@code='x'])">
     		<xsl:choose>
     			<xsl:when test="$locfilter=@tag">
     				<xsl:copy-of select="."/>
     			</xsl:when>
     			<xsl:when test="$locfilter='all'">
     				<xsl:copy-of select="."/>
     			</xsl:when>
     			<xsl:otherwise/>
     		</xsl:choose>     		
     	</xsl:if>   		  		
  	</xsl:template>
  	
  <xsl:template match="datafield[@tag='852']">
  		<xsl:copy-of select="."/>
  	</xsl:template>

	<xsl:template match="*"/>
 	
  
</xsl:stylesheet>