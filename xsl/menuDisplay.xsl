<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="">

	 <xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8"/>
	 <xsl:preserve-space elements="xsl:text"/>
	 
	 
	<xsl:template match="/">
		<div class="menugrp">
			<strong>Browse:</strong>
			<xsl:call-template name="author"/>
			<xsl:call-template name="title"/>
			<xsl:call-template name="printer"/>
			<xsl:call-template name="printerloc"/>
		</div>
		<div class="menugrp">
			<xsl:call-template name="options">
				<xsl:with-param name="op">
					<xsl:text>print</xsl:text>
				</xsl:with-param>
			</xsl:call-template>
			<xsl:call-template name="options">
				<xsl:with-param name="op">
					<xsl:text>email</xsl:text>
				</xsl:with-param>
			</xsl:call-template>
			<xsl:call-template name="options">
				<xsl:with-param name="op">
					<xsl:text>save</xsl:text>
				</xsl:with-param>
			</xsl:call-template>      
			<div class="menuitem">with expanded bibliographical refs <input type="checkbox" id="expandedbib"/></div>              
		</div>
	</xsl:template>	
	
	<xsl:template name="options">
		<xsl:param name="op"/>
		<div class="menuitem">
			<a href="#">
				<xsl:attribute name="onclick">
					<xsl:text>submitForm('</xsl:text><xsl:value-of select="$op"/><xsl:text>')</xsl:text>
				</xsl:attribute>
				<xsl:choose>
					<xsl:when test="$op = 'print'"><xsl:text>Print Record</xsl:text><img src="/istc/images/link_print.gif" alt="" width="27" height="21" border="0" align="middle"/></xsl:when>	
					<xsl:when test="$op = 'email'"><xsl:text>Email Record</xsl:text><img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></xsl:when>
					<xsl:when test="$op = 'save'"><xsl:text>Save Record</xsl:text><img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/></xsl:when>			
				</xsl:choose>
			</a>
		</div><br/>
	</xsl:template>
		
	<xsl:template name="author">
		<xsl:if test="//datafield[@tag='100']">		
			<xsl:variable name="author">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='100']/subfield[@code='a']">
						<xsl:value-of select="translate(//datafield[@tag='100']/subfield[@code='a'], '[]', '')"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="translate(//datafield[@tag='100'], '[]', '')"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>				
			<div class="menuitem">
				<strong>Author</strong>
				<a>			
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.creator&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$author"/>
					</xsl:attribute>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/><br/>
		 		</a>
			</div><br/>
			<div class="menuitemextra">
				<a>			
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.creator&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$author"/>
					</xsl:attribute>
		 			<span class="extralink"><xsl:value-of select="$author"/></span>	
		 		</a>
			</div><br/>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']|//datafield[@tag='130']/subfield[@code='a']">
			<xsl:variable name="title">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:value-of select="translate(//datafield[@tag='245']/subfield[@code='a'], '[]', '')"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="translate(//datafield[@tag='130']/subfield[@code='a'], '[]', '')"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>		
			<div class="menuitem">
				<strong>Title</strong>				
				<a>
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.title&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$title"/>
					</xsl:attribute>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/><br/>	
		 		</a>
			</div><br/>
			<div class="menuitemextra">
				<a>
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.title&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$title"/>
					</xsl:attribute>
					<xsl:choose>
						<xsl:when test="string-length($title)&gt;25">
							<xsl:value-of select="substring($title, 1, 25)"/><xsl:text>...</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$title"/>
						</xsl:otherwise>
					</xsl:choose>				
		 		</a>
			</div><br/>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="printer">
		<xsl:if test="//datafield[@tag='260']/subfield[@code='b']">
			<xsl:variable name="printer">				
				<xsl:value-of select="translate(//datafield[@tag='260']/subfield[@code='b'], '[]', '')"/>
			</xsl:variable>		
			<div class="menuitem">
				<strong>Printer</strong>				
				<a>	
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.publisher&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printer"/>
					</xsl:attribute>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>	 			
		 		</a>
		 	</div><br/>
		 	<div class="menuitemextra">
		 		<a>	
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=dc.publisher&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printer"/>
					</xsl:attribute>
					<xsl:choose>
						<xsl:when test="string-length($printer)&gt;25">
							<xsl:value-of select="substring($printer, 1, 25)"/><xsl:text>...</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$printer"/>
						</xsl:otherwise>
					</xsl:choose>			 			
		 		</a>
		 	</div><br/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="printerloc">
		<xsl:if test="//datafield[@tag='260']/subfield[@code='a']">
			<xsl:variable name="printerloc">				
				<xsl:value-of select="translate(//datafield[@tag='260']/subfield[@code='a'], '[]', '')"/>
			</xsl:variable>		
			<div class="menuitem">
				<strong>Printer Location</strong>
				<a>
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=bib.originPlace&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printerloc"/>
					</xsl:attribute>
					<img src="/istc/images/int_link.gif" alt="" width="27" height="21" border="0" align="middle"/>
		 		</a>
			 </div><br/>
			 <div class="menuitemextra">
			 	<a>
					<xsl:attribute name="href">
						<xsl:text>/istc/search/?operation=scan&amp;fieldidx1=bib.originPlace&amp;fieldrel1=exact&amp;fieldcont1=</xsl:text><xsl:value-of select="$printerloc"/>
					</xsl:attribute>
		 			<xsl:value-of select="$printerloc"/>
		 		</a>
			 </div><br/>
		</xsl:if>
	</xsl:template>
 	 
</xsl:stylesheet>

	
