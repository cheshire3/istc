<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="">

	 <xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8"/>
	 <xsl:preserve-space elements="xsl:text"/>
	 
	 
	<xsl:template match="/">
		<xsl:call-template name="author"/>
		<xsl:call-template name="title"/>
		<xsl:call-template name="printer"/>
		<xsl:call-template name="printerloc"/>
	</xsl:template>	
	
	
	
	<xsl:template name="author">
		<xsl:if test="//datafield[@tag='100']">		
			<xsl:variable name="author">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='100']/subfield[@code='a']">
						<xsl:value-of select="//datafield[@tag='100']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="//datafield[@tag='100']"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>		
			<tr>
				<td align="right" valign="middle" class="text">
					<strong>Browse Author</strong>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>
				</td>
			</tr>
			<tr class="menusubheading">
				<td align="right">
					<a>
						<xsl:attribute name="href">
							<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=c3.idx-author&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$author"/>
						</xsl:attribute>
			 			<xsl:value-of select="$author"/>
			 		</a>
			 	</td>
			</tr>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']|//datafield[@tag='130']/subfield[@code='a']">
			<xsl:variable name="title">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:value-of select="//datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="//datafield[@tag='130']/subfield[@code='a']"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>		
			<tr>
				<td align="right" valign="middle" class="text">
					<strong>Browse Title</strong>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>
				</td>
			</tr>
			<tr class="menusubheading">
				<td align="right">
					<a>
						<xsl:attribute name="href">
							<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=c3.idx-title&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$title"/>
						</xsl:attribute>
						<xsl:choose>
							<xsl:when test="string-length($title)&gt;35">
								<xsl:value-of select="substring($title, 1, 35)"/><xsl:text>...</xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="$title"/>
							</xsl:otherwise>
						</xsl:choose>
			 			
			 		</a>
			 	</td>
			</tr>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="printer">
		<xsl:if test="//datafield[@tag='260']/subfield[@code='b']">
			<xsl:variable name="printer">				
				<xsl:value-of select="//datafield[@tag='260']/subfield[@code='b']"/>
			</xsl:variable>		
			<tr>
				<td align="right" valign="middle" class="text">
					<strong>Browse Printer</strong>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>
				</td>
			</tr>
			<tr class="menusubheading">
				<td align="right">
					<a>
						<xsl:attribute name="href">
							<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=c3.idx-printer&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printer"/>
						</xsl:attribute>
			 			<xsl:value-of select="$printer"/>
			 		</a>
			 	</td>
			</tr>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="printerloc">
		<xsl:if test="//datafield[@tag='260']/subfield[@code='a']">
			<xsl:variable name="printerloc">				
				<xsl:value-of select="//datafield[@tag='260']/subfield[@code='a']"/>
			</xsl:variable>		
			<tr>
				<td align="right" valign="middle" class="text">
					<strong>Browse Printer Location</strong>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>
				</td>
			</tr>
			<tr class="menusubheading">
				<td align="right">
					<a>
						<xsl:attribute name="href">
							<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=c3.idx-location&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printerloc"/>
						</xsl:attribute>
			 			<xsl:value-of select="$printerloc"/>
			 		</a>
			 	</td>
			</tr>
		</xsl:if>
	</xsl:template>
 
	 
</xsl:stylesheet>

	
