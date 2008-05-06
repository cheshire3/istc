<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8" />
	<xsl:preserve-space elements="*" />
	
	<xsl:template match="/">
		<div id="formDiv" name="form" class="formDiv" onscroll="hideAllMenus()">
			<form id="eadForm" name="eadForm" action="#">
			<p><strong>ISTC Number:</strong><br/>
				<xsl:choose>
					<xsl:when test="controlfield[@tag='001']">
						<xsl:apply-templates select="controlfield[@tag='001']"/>
					</xsl:when>
					<xsl:otherwise>
						<input class="menuField" type="text" onfocus="setCurrent(this);" name="controlfield[@tag='001']" id="ISTCNo" size="39"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			<!--<p><strong>Author(s):</strong><br/>
				<xsl:choose>
					<xsl:when test="controlfield[@tag='100']|controlfield[@tag='130']">
						<xsl:apply-templates select="controlfield[@tag='100']|controlfield[@tag='130']"/>
					</xsl:when>
					<xsl:otherwise>
						<input class="menuField" type="text" onfocus="setCurrent(this);" name="controlfield[@tag='001']" id="ISTCNo" size="39"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			
			-->
			<p><strong>Title:</strong><br/>
				<xsl:choose>
					<xsl:when test="datafield[@tag='245']/subfield[@code='a']">
						<xsl:apply-templates select="datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<input class="menuField" type="text" onfocus="setCurrent(this);" name="datafield[@tag='245']/subfield[@code='a']" id="title" size="39"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			
			
			</form>
		</div>
	</xsl:template>
	
	<xsl:template match="controlfield[@tag='001']">
		<input class="menuField" type="text" onfocus="setCurrent(this);" name="controlfield[@tag='001']" id="ISTCNo" size="39">
			<xsl:value-of select="."/>
		</input>
	</xsl:template>
	
	<xsl:template match="datafield[@tag='245']/subfield[@code='a']">
		<input class="menuField" type="text" onfocus="setCurrent(this);" name="datafield[@tag='245']/subfield[@code='a']" id="title" size="39">
			<xsl:value-of select="."/>
		</input>
	</xsl:template>
	
</xsl:stylesheet>