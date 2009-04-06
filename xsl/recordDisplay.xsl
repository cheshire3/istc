<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="http://www.cheshire3.org"
				xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str"
                xmlns:c3fn="http://www.cheshire3.org/ns/xsl/">

	<xsl:param name="format">
		<xsl:text>screen</xsl:text>
	</xsl:param>
	
	<xsl:param name="expand">
		<xsl:text>false</xsl:text>
	</xsl:param>

	<xsl:param name="locations">
		<xsl:text>all</xsl:text>
	</xsl:param>

	<xsl:param name="output">
		<xsl:choose>
			<xsl:when test="$format='screen' or $format='print'">
				<xsl:text>xml</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>text</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:param>
	
	<xsl:param name="encoding">
		<xsl:choose>
			<xsl:when test="$format='screen' or $format='print'">
				<xsl:text>UTF-8</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>ascii</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:param>
	
	<xsl:variable name="newline">
		<xsl:text>
</xsl:text>
	</xsl:variable>
	
	<xsl:variable name="tab">
		<xsl:text>	</xsl:text>
	</xsl:variable>
	
	 <xsl:output method="$output" omit-xml-declaration="yes" encoding="ascii"/>
	 <xsl:preserve-space elements="xsl:text"/>
	 
	 <xsl:variable name="ilc">
			<xsl:if test="//datafield[@tag='510']/subfield[@code='a']">
				<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
					<xsl:if test="starts-with(., 'ILC')">
						<xsl:value-of select="substring-after(., ' ')"/>
					</xsl:if>
				</xsl:for-each>
			</xsl:if>
			<xsl:else>
				<xsl:text></xsl:text>
			</xsl:else>
	</xsl:variable>
	
	<xsl:variable name="lib">
		<xsl:text>Reproductions of the watermarks found in the paper used in this edition are provided by the Koninklijke Bibliotheek, National Library of the Netherlands</xsl:text>
	</xsl:variable>

	 
	 <lang:name abbr="eng">English</lang:name>
	 <lang:name abbr="heb">Hebrew</lang:name>
	 <lang:name abbr="bre">Breton</lang:name>
	 <lang:name abbr="cat">Catalan</lang:name>
	 <lang:name abbr="chu">Church Slavonic</lang:name>
	 <lang:name abbr="cze">Czech</lang:name>
	 <lang:name abbr="dan">Danish</lang:name>
	 <lang:name abbr="dut">Dutch</lang:name>
	 <lang:name abbr="fri">Frisian</lang:name>
	 <lang:name abbr="fre">French</lang:name>
	 <lang:name abbr="frm">French</lang:name>
	 <lang:name abbr="ger">German</lang:name>
	 <lang:name abbr="grc">Greek</lang:name>
	 <lang:name abbr="ita">Italian</lang:name>
	 <lang:name abbr="lat">Latin</lang:name>
	 <lang:name abbr="por">Portuguese</lang:name>
	 <lang:name abbr="pro">Provençal / Occitan</lang:name>
	 <lang:name abbr="sar">Sardinian</lang:name>
	 <lang:name abbr="spa">Spanish</lang:name>
	 <lang:name abbr="scr">Croatian</lang:name>
	 <lang:name abbr="swe">Swedish</lang:name>

	 
	<xsl:template match="/">
		<xsl:choose>	
			<xsl:when test="$output='xml'">	
				<xsl:if test="$format='screen'">
					<div class="counter">%counter%</div>
					<div class="recordnav">%nav%</div><br/>
				</xsl:if>
				<table cellpadding = "5">			
					<xsl:call-template name="contents"/>
				</table>
				<xsl:if test="$format='screen'">
					<div class="recordnav">%nav%</div>
					<form id="mainform" action="search.html" method="get">
						<input type="hidden" id="opvalue" name="operation" value="print"/>
						<input type="hidden" id="expand" name="expand" value="false"/>
						<input type="hidden" id="locations" name="locations">
							<xsl:attribute name="value">
								<xsl:value-of select="$locations"/>
							</xsl:attribute>
						</input>
						<input type="hidden" name="istc">
							<xsl:attribute name="value">
								<xsl:value-of select="//controlfield[@tag='001']"/>
							</xsl:attribute>
						</input>
					</form>				
				</xsl:if>	
			</xsl:when>
			<xsl:otherwise>		
				<xsl:text>\par \pard\plain \ltrpar\s1\ql\rtlch\afs24\lang255\ltrch\dbch\af2\langfe255\hich\fs24\lang1033\loch\fs24\lang1033 
\par \pard\plain \ltrpar\s1\ql\rtlch\afs24\lang255\ltrch\dbch\af2\langfe255\hich\fs24\lang1033\loch\fs24\lang1033 
\par \trowd\trql\trleft0\trpaddft3\trpaddt29\trpaddfl3\trpaddl29\trpaddfb3\trpaddb29\trpaddfr3\trpaddr29\cellx2250\cellx9975</xsl:text>
  				<xsl:call-template name="contents"/>
				<xsl:text>\par</xsl:text>
				<xsl:value-of select="$newline"/>
			</xsl:otherwise>
		</xsl:choose>	
	</xsl:template>

	<xsl:template name="contents">	
		<xsl:call-template name="author"/>	
		<xsl:call-template name="heading"/>
		<xsl:call-template name="title"/>
		<xsl:call-template name="imprint"/>
		<xsl:call-template name="imprint_extra"/>
		<xsl:call-template name="format"/>		
	<!--	<xsl:call-template name="language"/> 		-->
		<xsl:call-template name="istcNumber"/>
		<xsl:call-template name="references"/>
		<xsl:call-template name="reproductions"/> 
		<xsl:call-template name="notes"/>
		<xsl:call-template name="locations"/>
		
	</xsl:template>

 	<xsl:template name="author">
 		<xsl:choose>
	 		<xsl:when test="//datafield[@tag='100']">
	 			<xsl:variable name="label">
	 				<xsl:text>Author:</xsl:text>
	 			</xsl:variable>
	 			<xsl:variable name="value">
	 				<xsl:choose>
						<xsl:when test="//datafield[@tag='100']/subfield[@code='a']">
							<xsl:value-of select="//datafield[@tag='100']/subfield[@code='a']"/>
						</xsl:when>
						<xsl:otherwise test="//datafield[@tag='100']">
							<xsl:value-of select="//datafield[@tag='100']"/>
						</xsl:otherwise>
					</xsl:choose>
	 			</xsl:variable>
	 			<xsl:choose>
	 				<xsl:when test="$output='xml'">
						<tr>
							<td class="label">
								<xsl:value-of select="$label"/>
							</td>
							<td>
								<xsl:value-of select="$value"/>
							</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$label"/>
							<xsl:with-param name="value" select="$value"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="//datafield[@tag='700']">
				<xsl:text>Not Implemented in recordDisplay.xsl</xsl:text>
			</xsl:when>
		</xsl:choose>
	</xsl:template>


 	<xsl:template name="heading">
 		<xsl:if test="//datafield[@tag='130']">
 			<xsl:variable name="label">
 				<xsl:text>Heading:</xsl:text>
 			</xsl:variable>
 			<xsl:variable name="value">
 				<xsl:choose>
 					<xsl:when test="//datafield[@tag='130']/subfield[@code='a']">
 						<xsl:value-of select="//datafield[@tag='130']/subfield[@code='a']" />
 					</xsl:when>
 					<xsl:otherwise test="//datafield[@tag='130']">
 						<xsl:value-of select="//datafield[@tag='130']" />
 					</xsl:otherwise>
 				</xsl:choose>
 			</xsl:variable>
 			<xsl:choose>
 				<xsl:when test="$output='xml'">
 					<tr>
 						<td class="label">
 							<xsl:value-of select="$label" />
 						</td>
 						<td>
 							<xsl:value-of select="$value" />
 						</td>
 					</tr>
 				</xsl:when>
 				<xsl:otherwise>
 					<xsl:call-template name="textView">
 						<xsl:with-param name="label" select="$label" />
 						<xsl:with-param name="value" select="$value" />
 					</xsl:call-template>
 				</xsl:otherwise>
 			</xsl:choose>
 		</xsl:if>
 	</xsl:template>


 	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']">
			<xsl:variable name="label">
				<xsl:text>Title:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:value-of select="//datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
				</xsl:choose>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
					<td class="label"><xsl:value-of select="$label"/></td>
					<td>
						<xsl:value-of select="$value"/>
					</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="imprint">
		<xsl:if test="//datafield[@tag='260']">
			<xsl:variable name="label">
				<xsl:text>Imprint:</xsl:text>
			</xsl:variable>		
			<xsl:variable name="value">	
				<xsl:for-each select="//datafield[@tag='260']">	
					<xsl:choose>
						<xsl:when test="position() = 1">								
							<xsl:if test="subfield[@code='a']">
								<xsl:value-of select="subfield[@code='a']"/><xsl:text>: </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='b']">
								<xsl:value-of select="subfield[@code='b']"/><xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='c']">
								<xsl:value-of select="subfield[@code='c']"/><xsl:text> </xsl:text>
							</xsl:if>					
						</xsl:when>
					</xsl:choose>
				</xsl:for-each>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
					<td class="label"><xsl:value-of select="$label"/></td>
					<td>
						<xsl:value-of select="$value"/><br /><!-- <xsl:value-of select="$value2"/><xsl:value-of select="$value3"/> -->
					</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="imprint_extra">
		<xsl:if test="count(//datafield[@tag='260']) &gt; 1">
			<xsl:variable name="label">
				<xsl:text> </xsl:text>
			</xsl:variable>		
			<xsl:variable name="value">	
				<xsl:for-each select="//datafield[@tag='260']">	
					<xsl:choose>
						 <xsl:when test="position() = 2">		
							<xsl:text>Also recorded as </xsl:text>
							<xsl:if test="subfield[@code='a']">
								<xsl:value-of select="subfield[@code='a']"/><xsl:text>: </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='b']">
								<xsl:value-of select="subfield[@code='b']"/><xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='c']">
								<xsl:value-of select="subfield[@code='c']"/><xsl:text>  </xsl:text>
							</xsl:if>
							<xsl:text>and </xsl:text>
						</xsl:when>
						<xsl:when test="position() &gt; 2">					
							<xsl:if test="subfield[@code='a']">
								<xsl:value-of select="subfield[@code='a']"/><xsl:text>: </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='b']">
								<xsl:value-of select="subfield[@code='b']"/><xsl:text>, </xsl:text>
							</xsl:if>
							<xsl:if test="subfield[@code='c']">
								<xsl:value-of select="subfield[@code='c']"/><xsl:text>  </xsl:text>
							</xsl:if>	
							<xsl:text>and </xsl:text>						
						</xsl:when>
					</xsl:choose>
				</xsl:for-each>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
					<td class="label"><xsl:value-of select="$label"/></td>
					<td>
						<xsl:value-of select="substring($value, 0, string-length($value)-5)"/><br /><!-- <xsl:value-of select="$value2"/><xsl:value-of select="$value3"/> -->
					</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="substring($value, 0, string-length($value)-5)"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
<!-- 	<xsl:template name="imprint">
		<xsl:if test="//datafield[@tag='260'][position() $gt; 1]">
			<xsl:variable name="label">
				<xsl:text>Imprint:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:for-each select="//datafield[@tag='260'][position() $gt; 1]">
					<xsl:if test="subfield[@code='a']">
						<xsl:value-of select="subfield[@code='a']"/><xsl:text>: </xsl:text>
					</xsl:if>
					<xsl:if test="subfield[@code='b']">
						<xsl:value-of select="subfield[@code='b']"/><xsl:text>, </xsl:text>
					</xsl:if>
					<xsl:if test="subfield[@code='c']">
						<xsl:value-of select="subfield[@code='c']"/><xsl:text> </xsl:text>
					</xsl:if>
					<xsl:value-of select="$newline"/>
					<br/>
				</xsl:for-each>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
					<td class="label"><xsl:value-of select="$label"/></td>
					<td>
						<xsl:value-of select="$value"/>
					</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template> -->
    
	
	<xsl:template name="format">
		<xsl:if test="//datafield[@tag='300']/subfield">
			<xsl:variable name="label">
				<xsl:text>Format:</xsl:text>
			</xsl:variable>
			 <xsl:variable name="ref">
				<xsl:value-of select="//datafield[@tag='300']/subfield"/>
			</xsl:variable> 
			<xsl:variable name="value">
				<xsl:value-of select="c3fn:format(//datafield[@tag='300']/subfield/text())"/>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<td>
							<xsl:call-template name="formatReplace">
								<xsl:with-param name="string">
									<xsl:value-of select="normalize-space($value)"/>
								</xsl:with-param>
							</xsl:call-template>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="stringFormat">
							<xsl:call-template name="formatReplace">
								<xsl:with-param name="string">
									<xsl:value-of select="normalize-space($value)"/>
								</xsl:with-param>
							</xsl:call-template>
					</xsl:variable>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$stringFormat"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="formatReplace">
		<xsl:param name="string"/>
		<xsl:choose>
			<xsl:when test="$output='xml'">
				<xsl:choose>
					<xsl:when test="substring-before($string, '&lt;sup&gt;')">
						<text><xsl:value-of select="substring-before($string, '&lt;sup&gt;')"/></text>
						<sup>
							<xsl:value-of select="substring-before(substring-after($string, '&lt;sup&gt;'), '&lt;/sup&gt;')"/>
						</sup>
						<xsl:if test="substring-after($string, '&lt;/sup&gt;')">
						 	<xsl:call-template name="formatReplace">
								<xsl:with-param name="string">
									<xsl:value-of select="substring-after($string, '&lt;/sup&gt;')"/>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<text><xsl:value-of select="$string"/></text>
					</xsl:otherwise>			
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:choose>
					<xsl:when test="substring-before($string, '&lt;sup&gt;')">
						<text>
							<xsl:value-of select="substring-before($string, '&lt;sup&gt;')"/>
							<xsl:value-of select="substring-before(substring-after($string, '&lt;sup&gt;'), '&lt;/sup&gt;')"/>
						</text>
						<xsl:if test="substring-after($string, '&lt;/sup&gt;')">
						 	<xsl:call-template name="formatReplace">
								<xsl:with-param name="string">
									<xsl:value-of select="substring-after($string, '&lt;/sup&gt;')"/>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:if>
					</xsl:when>
					<xsl:otherwise>
						<text><xsl:value-of select="$string"/></text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>	
	</xsl:template>

	<xsl:template name="language">
		<xsl:variable name="label">
			<xsl:text>Language:</xsl:text>
		</xsl:variable>
		<xsl:variable name="lang">
			<xsl:value-of select="substring(//controlfield[@tag='008']/text(), 36, 3)"/>
		</xsl:variable>
		<xsl:variable name="value">
			<xsl:choose>
				<xsl:when test="document('')/xsl:stylesheet/lang:name[@abbr=$lang]"> 
					<xsl:value-of select="document('')/xsl:stylesheet/lang:name[@abbr=$lang]"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$lang"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="$output='xml'">
				<tr>
					<td class="label"><xsl:value-of select="$label"/></td>
					<td>
					 	<xsl:value-of select="$value"/>
					</td>
				</tr>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="textView">
					<xsl:with-param name="label" select="$label"/>
					<xsl:with-param name="value" select="$value"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>


	<xsl:template name="istcNumber">
		<xsl:if test="//controlfield[@tag='001']">
			<xsl:variable name="label">
				<xsl:text>ISTC No.:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:value-of select="//controlfield[@tag='001']"/>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<td>
							<xsl:value-of select="$value"/>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="references">
		<xsl:if test="//datafield[@tag='510']">
			<xsl:variable name="label">
				<xsl:text>References:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:choose>
					<xsl:when test="$expand='true'">
						<xsl:text>%fullrefs%</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
							<xsl:choose>
								<xsl:when test="$format='screen'">
									<xsl:choose>
										<xsl:when test="starts-with(., 'BSB-Ink')">		
											<xsl:choose>
												<xsl:when test="contains(., '(')">
													<xsl:text>&lt;a href="http://mdzx.bib-bvb.de/bsbink/Ausgabe_</xsl:text><xsl:value-of select="substring-before(substring-after(., 'BSB-Ink '), ' ')"/><xsl:text>.html" target="_new"></xsl:text><xsl:value-of select="."/><xsl:text>&lt;/a>; </xsl:text>				
												</xsl:when>
												<xsl:when test="contains(., ',')">
													<xsl:text>&lt;a href="http://mdzx.bib-bvb.de/bsbink/Ausgabe_</xsl:text><xsl:value-of select="substring-before(substring-after(., 'BSB-Ink '), ',')"/><xsl:text>.html" target="_new"></xsl:text><xsl:value-of select="."/><xsl:text>&lt;/a>; </xsl:text>				
												</xsl:when>
												<xsl:otherwise>
													<xsl:text>&lt;a href="http://mdzx.bib-bvb.de/bsbink/Ausgabe_</xsl:text><xsl:value-of select="substring-after(., 'BSB-Ink ')"/><xsl:text>.html" target="_new"></xsl:text><xsl:value-of select="."/><xsl:text>&lt;/a>; </xsl:text>				
												</xsl:otherwise>											
											</xsl:choose>																								
										</xsl:when>
										<xsl:otherwise>
											<xsl:value-of select="."/><xsl:text>; </xsl:text>
										</xsl:otherwise>
									</xsl:choose>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="."/><xsl:text>; </xsl:text>
								</xsl:otherwise>
							</xsl:choose>
							
						</xsl:for-each>
					</xsl:otherwise>					
				</xsl:choose>				
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">			
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<xsl:choose>
							<xsl:when test="$expand='false'">
								<td>
									<div style="display: block" id="abbrRefs">
										<xsl:value-of select="substring($value, 0, string-length($value)-1)"/>
										<xsl:if test="$format='screen'">	
											<br /><a href="javascript:expandRefs()">expand references</a>
										</xsl:if>
									</div>
									<xsl:if test="$format='screen'">	
										<div style="display: none" id="fullRefs">
											<xsl:text>%fullrefs%</xsl:text>
											<br />
											<a href="javascript:collapseRefs()">collapse references</a>
										</div>
									</xsl:if>
								</td>
							</xsl:when>
							<xsl:otherwise>
								<td>
									<xsl:text>%fullrefs%</xsl:text>
								</td>
							</xsl:otherwise>
						</xsl:choose>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="substring($value, 0, string-length($value)-1)"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="reproductions">
		<xsl:if test="//datafield[@tag='530']">
			<xsl:variable name="label">
				<xsl:text>Reproductions:</xsl:text>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label">
							<xsl:value-of select="$label"/>
						</td>
						<td>
							<xsl:for-each select="//datafield[@tag='530']">							
								<xsl:for-each select="subfield[not(@code='u')]">
									<xsl:value-of select="." />
								</xsl:for-each>
															
								<xsl:choose>
									<xsl:when test="$format='screen' and subfield[@code='u']">
										<xsl:text> </xsl:text>
										<a target="_new">
											<xsl:attribute name="href">
												<xsl:value-of select="subfield[@code='u']" />
											</xsl:attribute>
											<xsl:text>Click here to visit the website</xsl:text>
										</a>
									</xsl:when>
									<xsl:when test="subfield[@code='u']">
										<xsl:text> [</xsl:text><xsl:value-of select="subfield[@code='u']" /><xsl:text>]</xsl:text>
									</xsl:when>
								</xsl:choose>
								<br/>
							</xsl:for-each>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="value">
						<xsl:for-each select="//datafield[@tag='530']">						
							<xsl:for-each select="subfield[not(@code='u')]">
								<xsl:value-of select="." />
							</xsl:for-each>
							 <br/>	 
							 <xsl:if test="not($format='screen') and subfield[@code='u']">
								<xsl:text>  [</xsl:text><xsl:value-of select="subfield[@code='u']" /><xsl:text>]</xsl:text>
							</xsl:if> 													
						</xsl:for-each>
					</xsl:variable>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="notes">
		<xsl:if test="//datafield[@tag='500']|//datafield[@tag='505']">
			<xsl:variable name="label">
				<xsl:text>Notes:</xsl:text>
			</xsl:variable>	
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<td>
							<xsl:for-each select="//datafield[@tag='500']">
								<xsl:choose>
									<xsl:when test="contains(., $lib) and $ilc">
										<xsl:value-of select="."/><br/>
										<xsl:if test="$format='screen'">
											<a target="_new">
												<xsl:attribute name="href">
													<xsl:text>http://watermark.kb.nl/findWM.asp?biblio=ILC </xsl:text>
													<xsl:choose>
														<xsl:when test="string-length($ilc) &lt; 4">
															<xsl:text>0</xsl:text><xsl:value-of select="$ilc"/>
														</xsl:when>
														<xsl:otherwise>
															<xsl:value-of select="$ilc"/>
														</xsl:otherwise>
													</xsl:choose>
													<xsl:text>&amp;max=50&amp;boolean=AND&amp;search2=Search&amp;exact=TRUE</xsl:text>
												</xsl:attribute>
												<xsl:text>Click here to visit the website</xsl:text>
											</a>
										</xsl:if>
										<br/><br/>
									</xsl:when>
									<xsl:otherwise>
										<xsl:choose>
											<xsl:when test="contains(., '~~')">
												<xsl:call-template name="formatReplace">
													<xsl:with-param name="string">
														<xsl:value-of select="c3fn:format(.//text())"/>
														</xsl:with-param>
												</xsl:call-template>
											</xsl:when>
											<xsl:otherwise>
												<xsl:value-of select="."/>
											</xsl:otherwise>
										</xsl:choose>										
										<br/>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:for-each>
							<xsl:for-each select="//datafield[@tag='505']">
								<xsl:choose>
									<xsl:when test="contains(., '~~')">
										<xsl:call-template name="formatReplace">
											<xsl:with-param name="string">
												<xsl:value-of select="c3fn:format(.//text())"/>
												</xsl:with-param>
										</xsl:call-template>
									</xsl:when>
									<xsl:otherwise>
										<xsl:value-of select="."/>
									</xsl:otherwise>
								</xsl:choose>										
								<br/>
							</xsl:for-each>							
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="value">				
						<xsl:for-each select="//datafield[@tag='500']/subfield">	
							<xsl:choose>
								<xsl:when test="contains(., '~~')">			
									<xsl:call-template name="formatReplace">
										<xsl:with-param name="string">
											<xsl:value-of select="c3fn:format(.//text())"/>
											</xsl:with-param>
									</xsl:call-template>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="."/>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:for-each>
						<xsl:for-each select="//datafield[@tag='505']/subfield">
							<xsl:choose>
								<xsl:when test="contains(., '~~')">	
									<xsl:call-template name="formatReplace">
										<xsl:with-param name="string">
											<xsl:value-of select="c3fn:format(.//text())"/>
											</xsl:with-param>
									</xsl:call-template>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="."/>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:for-each>
					</xsl:variable>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>


<!-- 	<xsl:template name="shelfmark">
		<xsl:if test="//datafield[@tag='852']">
			<xsl:variable name="label">
				<xsl:text>British Library Shelfmark:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:for-each select="//datafield[@tag='852']/subfield">
					<xsl:value-of select="."/><xsl:text> </xsl:text>
				</xsl:for-each>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<td>
							<xsl:value-of select="$value"/>
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
						<xsl:with-param name="value" select="$value"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template> -->
	
	
	<xsl:template name="locations">
		<xsl:if test="((//datafield[@tag='852']|//datafield[@tag='951']|//datafield[@tag='995']|//datafield[@tag='957']|//datafield[@tag='997']|//datafield[@tag='954']|//datafield[@tag='955']|//datafield[@tag='996']|//datafield[@tag='952']|//datafield[@tag='958']|//datafield[@tag='953']|//datafield[@tag='994']) and $locations = 'all') or ($locations = 'germany' and //datafield[@tag='997'])">
			<xsl:variable name="label">
				<xsl:text>Locations:</xsl:text>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td><td></td>				
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="textView">
						<xsl:with-param name="label" select="$label"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
			
			<xsl:if test="(//datafield[@tag='951'] or //datafield[@tag='852']) and $locations = 'all'">
				<xsl:variable name="l1">
					<xsl:text>British Isles:</xsl:text>
				</xsl:variable>
			<!--  	<xsl:if test="//datafield[@tag='852']">
					<xsl:variable name="j">
						<xsl:for-each select="//datafield[@tag='852']">
							<xsl:for-each select="subfield[@code='j']">
								<xsl:value-of select="."/><xsl:text>, </xsl:text>
							</xsl:for-each>
						</xsl:for-each>
					</xsl:variable>
					<xsl:variable name="q">
						<xsl:for-each select="//datafield[@tag='852']">
							<xsl:for-each select="subfield[@code='q']">
								<xsl:text> </xsl:text><xsl:value-of select="."/>
							</xsl:for-each>
						</xsl:for-each>
					</xsl:variable>
				</xsl:if> -->
				
				<xsl:variable name="v1">
					<xsl:if test="//datafield[@tag='852']">
						<xsl:text>London, British Library  (</xsl:text>
					 	<xsl:for-each select="//datafield[@tag='852']">
					  	<xsl:variable name="j">
								<xsl:for-each select="subfield[@code='j']">
									<xsl:value-of select="."/><xsl:text>, </xsl:text>
								</xsl:for-each>
							</xsl:variable>
							<xsl:variable name="q">
								<xsl:for-each select="subfield[@code='q']">
									<xsl:text> </xsl:text><xsl:value-of select="."/>
								</xsl:for-each>
							</xsl:variable>						
							<xsl:choose>
								<xsl:when test="subfield[@code='q']">
									<xsl:value-of select="$j"/>
							  		<xsl:value-of select="$q"/>
						 		</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="substring($j, 0, string-length($j)-1)"/>
								</xsl:otherwise>
							</xsl:choose>
							<xsl:text>); </xsl:text>
						</xsl:for-each>
					</xsl:if>
					<xsl:for-each select="//datafield[@tag='951'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l1"/></td>					
						<td>
							<xsl:value-of select="substring($v1, 0, string-length($v1)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l1"/>
							<xsl:with-param name="value" select="substring($v1, 0, string-length($v1)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='995'] and $locations = 'all'">
				<xsl:variable name="l2">
					<xsl:text>Belgium:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v2">
					<xsl:for-each select="//datafield[@tag='995'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l2"/></td>					
						<td>
							<xsl:value-of select="substring($v2, 0, string-length($v2)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l2"/>
							<xsl:with-param name="value" select="substring($v2, 0, string-length($v2)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='957'] and $locations = 'all'">
				<xsl:variable name="l3">
					<xsl:text>France:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v3">
					<xsl:for-each select="//datafield[@tag='957'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l3"/></td>					
						<td>
							<xsl:value-of select="substring($v3, 0, string-length($v3)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l3"/>
							<xsl:with-param name="value" select="substring($v3, 0, string-length($v3)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>												
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='997'][not(subfield[@code='x'])] and ($locations = 'all' or $locations = 'germany')">
				<xsl:variable name="l4">
					<xsl:text>Germany:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v4">
					<xsl:for-each select="//datafield[@tag='997'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l4"/></td>					
						<td>
							<xsl:value-of select="substring($v4, 0, string-length($v4)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l4"/>
							<xsl:with-param name="value" select="substring($v4, 0, string-length($v4)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='954'] and $locations = 'all'">
				<xsl:variable name="l5">
					<xsl:text>Italy:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v5">
					<xsl:for-each select="//datafield[@tag='954'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l5"/></td>					
						<td>
							<xsl:value-of select="substring($v5, 0, string-length($v5)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l5"/>
							<xsl:with-param name="value" select="substring($v5, 0, string-length($v5)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='955'] and $locations = 'all'">
				<xsl:variable name="l6">
					<xsl:text>Spain/Portugal:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v6">
					<xsl:for-each select="//datafield[@tag='955'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l6"/></td>					
						<td>
							<xsl:value-of select="substring($v6, 0, string-length($v6)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l6"/>
							<xsl:with-param name="value" select="substring($v6, 0, string-length($v6)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='996'] and $locations = 'all'">
				<xsl:variable name="l7">
					<xsl:text>Netherlands:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v7">
					<xsl:for-each select="//datafield[@tag='996'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l7"/></td>					
						<td>
							<xsl:value-of select="substring($v7, 0, string-length($v7)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l7"/>
							<xsl:with-param name="value" select="substring($v7, 0, string-length($v7)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='952'] and $locations = 'all'">
				<xsl:variable name="l8">
					<xsl:text>U.S.A:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v8">
					<xsl:text>%usalocs%</xsl:text>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l8"/></td>					
						<td>
							<xsl:value-of select="$v8"/>			
						</td>
						</tr>				
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l8"/>
							<xsl:with-param name="value" select="$v8"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
<!--			<xsl:if test="//datafield[@tag='952'] and $locations = 'all'">
				<xsl:variable name="l8">
					<xsl:text>U.S.A:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v8">
					<xsl:for-each select="//datafield[@tag='952']">						
						<xsl:variable name="usaref">
							<xsl:value-of select="subfield[@code='a']/text()"/>
						</xsl:variable>
						<xsl:value-of select="document(concat('http://localhost/istc/search/search.html?operation=usareferences&amp;q=', $usaref))/record//full"/>
						<xsl:if test="subfield[@code='b']">
						<xsl:text> </xsl:text>
						<xsl:value-of select="subfield[@code='b']"/>
						</xsl:if>
						<xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l8"/></td>					
						<td>
							<xsl:value-of select="substring($v8, 0, string-length($v8)-1)"/>			
						</td>
						</tr>				
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l8"/>
							<xsl:with-param name="value" select="substring($v8, 0, string-length($v8)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>-->
			
			<xsl:if test="//datafield[@tag='958'] and $locations = 'all'">
				<xsl:variable name="l9">
					<xsl:text>Other Europe:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v9">
					<xsl:for-each select="//datafield[@tag='958'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l9"/></td>					
						<td>
							<xsl:value-of select="substring($v9, 0, string-length($v9)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l9"/>
							<xsl:with-param name="value" select="substring($v9, 0, string-length($v9)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='953'] and $locations = 'all'">
				<xsl:variable name="l10">
					<xsl:text>Other:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v10">
					<xsl:for-each select="//datafield[@tag='953'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l10"/></td>					
						<td>
							<xsl:value-of select="substring($v10, 0, string-length($v10)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l10"/>
							<xsl:with-param name="value" select="substring($v10, 0, string-length($v10)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='994'] and $locations = 'all'">
				<xsl:variable name="l11">
					<xsl:text>Doubtful:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v11">
					<xsl:for-each select="//datafield[@tag='994'][not(subfield[@code='x'])]">
						<xsl:value-of select="subfield[@code='a']"/>
						<xsl:choose>
							<xsl:when test="subfield[@code='b']">
								<xsl:text> </xsl:text>
								<xsl:value-of select="subfield[@code='b']"/>
								<xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>; </xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l11"/></td>					
						<td>
							<xsl:value-of select="substring($v11, 0, string-length($v11)-1)"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l11"/>
							<xsl:with-param name="value" select="substring($v11, 0, string-length($v11)-1)"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>				
			</xsl:if>
			
		</xsl:if>
	</xsl:template>


	<xsl:template name="textView">
	<xsl:param name="label"/>
	<xsl:param name="value"/>
		<xsl:text>\pard\intbl\pard\plain \intbl\ltrpar\s10\ql\rtlch\afs24\lang255\ab\ltrch\dbch\af2\langfe255\hich\fs24\lang1033\b\loch\fs24\lang1033\b {\rtlch \ltrch\loch\f1\fs24\lang1033\i0\b </xsl:text>
		<xsl:value-of select="$label"/>
		<xsl:text>}</xsl:text><xsl:value-of select="$newline"/>
		<xsl:text>\cell\pard\plain \intbl\ltrpar\s10\ql\rtlch\afs24\lang255\ltrch\dbch\af2\langfe255\hich\fs24\lang1033\loch\fs24\lang1033 {\rtlch \ltrch\loch\f1\fs24\lang1033\i0\b0 </xsl:text>
		<xsl:value-of select="$value"/>
		<xsl:text>}</xsl:text><xsl:value-of select="$newline"/>		
		<xsl:text>\cell\row\pard \pard\plain \ltrpar\s1\ql\rtlch\afs24\lang255\ltrch\dbch\af2\langfe255\hich\fs24\lang1033\loch\fs24\lang1033 </xsl:text><xsl:value-of select="$newline"/>
	</xsl:template>	
	

	<xsl:template name="replace">
		<xsl:param name="original"/>
		<xsl:param name="substring"/>
		<xsl:param name="replacement"/>
		<xsl:variable name="first">
			<xsl:choose>
				<xsl:when test="contains($original, $substring)">
					<xsl:value-of select="substring-before($original, $substring)"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$original"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="middle">
			<xsl:choose>
				<xsl:when test="contains($original, $substring)">
					<xsl:value-of select="$replacement"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text></xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="last">
			<xsl:choose>
				<xsl:when test="contains($original, $substring)">
					<xsl:choose>
						<xsl:when test="contains(substring-after($original, $substring), $substring)">
							<xsl:call-template name="replace">
								<xsl:with-param name="original">
									<xsl:value-of select="substring-after($original, $substring)"/>
								</xsl:with-param>
								<xsl:with-param name="substring">
									<xsl:value-of select="$substring"/>									
								</xsl:with-param>
								<xsl:with-param name="replacement">
									<xsl:value-of select="$replacement"/>									
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="substring-after($original, $substring)"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text></xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="concat($first, $middle, $last)"/>
	</xsl:template>
	


</xsl:stylesheet>