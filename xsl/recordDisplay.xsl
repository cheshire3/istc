<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="http://www.cheshire3.org"
				xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str">

	<xsl:param name="format">
		<xsl:text>screen</xsl:text>
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
	
	<xsl:variable name="newline">
		<xsl:text>
</xsl:text>
	</xsl:variable>
	
	<xsl:variable name="tab">
		<xsl:text>	</xsl:text>
	</xsl:variable>
	
	 <xsl:output method="$output" omit-xml-declaration="yes" encoding="UTF-8"/>
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
	 <lang:name abbr="ger">German</lang:name>
	 <lang:name abbr="ita">Italian</lang:name>
	 <lang:name abbr="lat">Latin</lang:name>
	 <lang:name abbr="por">Portuguese</lang:name>
	 <lang:name abbr="sar">Sardinian</lang:name>
	 <lang:name abbr="spa">Spanish</lang:name>
	 <lang:name abbr="swe">Swedish</lang:name>

	 
	<xsl:template match="/">
		<xsl:choose>	
			<xsl:when test="$output='xml'">	
				<table cellpadding = "5">
					<xsl:call-template name="contents"/>
				</table>	
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="contents"/>
			</xsl:otherwise>
		</xsl:choose>	
	</xsl:template>

	<xsl:template name="contents">
		<xsl:call-template name="author"/>	
		<xsl:call-template name="title"/>
		<xsl:call-template name="imprint"/>
		<xsl:call-template name="format"/>
		<xsl:call-template name="language"/>
		<xsl:call-template name="istcNumber"/>
		<xsl:call-template name="references"/>
		<xsl:call-template name="reproductions"/>
		<xsl:call-template name="notes"/>
		<xsl:call-template name="shelfmark"/>		
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
						<xsl:otherwise>
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

	
	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']|//datafield[@tag='130']/subfield[@code='a']">
			<xsl:variable name="label">
				<xsl:text>Title:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:value-of select="//datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="//datafield[@tag='130']/subfield[@code='a']"/>
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
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="imprint">
		<xsl:if test="//datafield[@tag='260']">
			<xsl:variable name="label">
				<xsl:text>Imprint:</xsl:text>
			</xsl:variable>
			<xsl:variable name="value">
				<xsl:for-each select="//datafield[@tag='260']">
					<xsl:for-each select="subfield">
						<xsl:value-of select="."/><xsl:text> </xsl:text>
					</xsl:for-each>
					<br />
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
	</xsl:template>
    
	
	<xsl:template name="format">
		<xsl:if test="//datafield[@tag='300']">
		<tr>
		<td class="label"><xsl:text>Format:</xsl:text></td>
		<td>
			<xsl:variable name="string1">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="//datafield[@tag='300']"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'4~~'"/>
					<xsl:with-param name="replacement" select="'4&lt;sup>to&lt;/sup>'"/>
				</xsl:call-template>		
			</xsl:variable>
			<xsl:variable name="string2">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="$string1"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'8~~'"/>
					<xsl:with-param name="replacement" select="'8&lt;sup>vo&lt;/sup>'"/>
				</xsl:call-template>		
			</xsl:variable> 					
			<xsl:variable name="string3">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="$string2"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'f~~'"/>
					<xsl:with-param name="replacement" select="'f&lt;sup>o&lt;/sup>'"/>
				</xsl:call-template>		
			</xsl:variable>
			<xsl:variable name="string4">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="$string3"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'bdsde'"/>
					<xsl:with-param name="replacement" select="'Broadside'"/>
				</xsl:call-template>		
			</xsl:variable>
			<xsl:variable name="string5">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="$string4"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'Bdsde'"/>
					<xsl:with-param name="replacement" select="'Broadside'"/>
				</xsl:call-template>		
			</xsl:variable>
			<xsl:variable name="string6">
				<xsl:call-template name="replace">
					<xsl:with-param name="original">
						<xsl:value-of select="$string5"/>
					</xsl:with-param>
					<xsl:with-param name="substring" select="'~~'"/>
					<xsl:with-param name="replacement" select="'&lt;sup>mo&lt;/sup>'"/>
				</xsl:call-template>		
			</xsl:variable>
			<xsl:value-of select="substring-before($string6, '&lt;sup>')"/>
			<sup>
				<xsl:value-of select="substring-after(substring-before($string6, '&lt;/sup>'), '&lt;sup>')"/>
			</sup>
			<xsl:value-of select="substring-after($string6, '&lt;/sup>')"/>
		</td>
		</tr>
		</xsl:if>
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
				<xsl:text>ISTC Number:</xsl:text>
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
				<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
			</xsl:variable>
			<xsl:choose>
				<xsl:when test="$output='xml'">			
					<tr>
						<td class="label"><xsl:value-of select="$label"/></td>
						<td>
							<div style="display: block" id="abbrRefs">
								<xsl:value-of select="$value"/>
								<xsl:if test="$format='screen'">	
									<br /><a href="javascript:expandRefs()">expand references</a>
								</xsl:if>
							</div>
							<xsl:if test="$format='screen'">	
								<div style="display: none" id="fullRefs">
									<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
										<xsl:variable name="ref">
											<xsl:value-of select="."/>
										</xsl:variable>
										<strong><xsl:value-of select="."/></strong><xsl:text>: </xsl:text>
										<xsl:value-of select="document(str:encode-uri(concat('http://localhost/istc/search/?operation=references&amp;q=', $ref), false()))/record//full"/>
										<br />
									</xsl:for-each>
									<a href="javascript:collapseRefs()">collapse references</a>
								</div>
							</xsl:if>
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
	
	
	<xsl:template name="reproductions">
		<xsl:if test="//datafield[@tag='530']">
			<tr>
				<td class="label">
					<xsl:text>Reproductions:</xsl:text>
				</td>
				<td>
					<xsl:for-each select="//datafield[@tag='530']">
						<xsl:for-each select="subfield[not(@code='u')]">
							<xsl:value-of select="." />
						</xsl:for-each>
						<br/>
						<xsl:if test="subfield[@code='u'] and $format='screen'">
							<a target="_new">
								<xsl:attribute name="href">
									<xsl:value-of select="subfield[@code='u']" />
								</xsl:attribute>
								<xsl:text>Click here to visit the website</xsl:text>
							</a>
						</xsl:if>
					</xsl:for-each>
				</td>
			</tr>
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
										<xsl:value-of select="."/><br/><br/>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:for-each>
							<xsl:for-each select="//datafield[@tag='505']">
								<xsl:value-of select="."/><br/><br/>
							</xsl:for-each>							
						</td>
					</tr>
				</xsl:when>
				<xsl:otherwise>
					<xsl:variable name="value">
						<xsl:for-each select="//datafield[@tag='500']">								
							<xsl:value-of select="."/><br/><br/>
						</xsl:for-each>
						<xsl:for-each select="//datafield[@tag='505']">
							<xsl:value-of select="."/><br/><br/>
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


	<xsl:template name="shelfmark">
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
	</xsl:template>
	
	
	<xsl:template name="locations">
		<xsl:if test="//datafield[@tag='951']|//datafield[@tag='995']|//datafield[@tag='957']|//datafield[@tag='997']|//datafield[@tag='954']|//datafield[@tag='955']|//datafield[@tag='996']|//datafield[@tag='952']|//datafield[@tag='958']|//datafield[@tag='953']|//datafield[@tag='994']">
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
			
			<xsl:if test="//datafield[@tag='951']">
				<xsl:variable name="l1">
					<xsl:text>British Isles:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v1">
					<xsl:for-each select="//datafield[@tag='951']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l1"/></td>					
						<td>
							<xsl:value-of select="$v1"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l1"/>
							<xsl:with-param name="value" select="$v1"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='995']">
				<xsl:variable name="l2">
					<xsl:text>Belgium:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v2">
					<xsl:for-each select="//datafield[@tag='995']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l2"/></td>					
						<td>
							<xsl:value-of select="$v2"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l2"/>
							<xsl:with-param name="value" select="$v2"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='957']">
				<xsl:variable name="l3">
					<xsl:text>France:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v3">
					<xsl:for-each select="//datafield[@tag='957']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l3"/></td>					
						<td>
							<xsl:value-of select="$v3"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l3"/>
							<xsl:with-param name="value" select="$v3"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>												
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='997']">
				<xsl:variable name="l4">
					<xsl:text>Germany:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v4">
					<xsl:for-each select="//datafield[@tag='997']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l4"/></td>					
						<td>
							<xsl:value-of select="$v4"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l4"/>
							<xsl:with-param name="value" select="$v4"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='954']">
				<xsl:variable name="l5">
					<xsl:text>Italy:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v5">
					<xsl:for-each select="//datafield[@tag='954']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">				
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l5"/></td>					
						<td>
							<xsl:value-of select="$v5"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l5"/>
							<xsl:with-param name="value" select="$v5"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='955']">
				<xsl:variable name="l6">
					<xsl:text>Spain/Portugal:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v6">
					<xsl:for-each select="//datafield[@tag='955']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l6"/></td>					
						<td>
							<xsl:value-of select="$v6"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l6"/>
							<xsl:with-param name="value" select="$v6"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='996']">
				<xsl:variable name="l7">
					<xsl:text>Netherlands:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v7">
					<xsl:for-each select="//datafield[@tag='996']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l7"/></td>					
						<td>
							<xsl:value-of select="$v7"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l7"/>
							<xsl:with-param name="value" select="$v7"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='952']">
				<xsl:variable name="l8">
					<xsl:text>U.S.A:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v8">
					<xsl:for-each select="//datafield[@tag='952']/subfield[@code='a']">
						<xsl:choose>
							 <xsl:when test="contains(current(), ' ')">
								<xsl:variable name="usaref"> 
									<xsl:value-of select="substring-before(current(), ' ')"/>								
							 	</xsl:variable>	
							 	<xsl:value-of select="document(concat('http://localhost/istc/search/?operation=usareferences&amp;q=', $usaref))/record//full"/><xsl:text>; </xsl:text>
							</xsl:when>
							<xsl:otherwise>
								<xsl:variable name="usaref">
									<xsl:value-of select="current()"/>
								</xsl:variable>
								<xsl:value-of select="document(concat('http://localhost/istc/search/?operation=usareferences&amp;q=', $usaref))/record//full"/><xsl:text>; </xsl:text>
							</xsl:otherwise> 		
						</xsl:choose>
					</xsl:for-each>
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
			
			<xsl:if test="//datafield[@tag='958']">
				<xsl:variable name="l9">
					<xsl:text>Other Europe:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v9">
					<xsl:for-each select="//datafield[@tag='958']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l9"/></td>					
						<td>
							<xsl:value-of select="$v9"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l9"/>
							<xsl:with-param name="value" select="$v9"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='953']">
				<xsl:variable name="l10">
					<xsl:text>Other:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v10">
					<xsl:for-each select="//datafield[@tag='953']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l10"/></td>					
						<td>
							<xsl:value-of select="$v10"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l10"/>
							<xsl:with-param name="value" select="$v10"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			
			<xsl:if test="//datafield[@tag='994']">
				<xsl:variable name="l11">
					<xsl:text>Doubtful:</xsl:text>
				</xsl:variable>
				<xsl:variable name="v11">
					<xsl:for-each select="//datafield[@tag='994']/subfield">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$output='xml'">
						<tr>
							<td align="right" class="subheader"><xsl:value-of select="$l11"/></td>					
						<td>
							<xsl:value-of select="$v11"/>
						</td>
						</tr>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="textView">
							<xsl:with-param name="label" select="$l11"/>
							<xsl:with-param name="value" select="$v11"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>				
			</xsl:if>
			
		</xsl:if>
	</xsl:template>


	<xsl:template name="textView">
		<xsl:param name="label"/>
		<xsl:param name="value"/>
		<xsl:value-of select="$label"/><xsl:value-of select="$tab"/><xsl:value-of select="$value"/><xsl:value-of select="$newline"/>
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