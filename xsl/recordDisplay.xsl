<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="">

	 <xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8"/>
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
		<table cellpadding = "5">
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
		</table>
	</xsl:template>


 	<xsl:template name="author">
 		<xsl:choose>
 		<xsl:when test="//datafield[@tag='100']">
		<tr>
		<td class="header"><xsl:text>Author:</xsl:text></td>
		<td>
		<xsl:choose>
			<xsl:when test="//datafield[@tag='100']/subfield[@code='a']">
				<xsl:value-of select="//datafield[@tag='100']/subfield[@code='a']"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="//datafield[@tag='100']"/>
			</xsl:otherwise>
		</xsl:choose>
		</td>
		</tr>
		</xsl:when>
		<xsl:when test="//datafield[@tag='700']">
			<xsl:text>Not Implemented in recordDisplay.xsl</xsl:text>
		</xsl:when>
		</xsl:choose>
	</xsl:template>

	
	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']|//datafield[@tag='130']/subfield[@code='a']">
		<tr>
		<td class="header"><xsl:text>Title:</xsl:text></td>
		<td>
			<xsl:if test="//datafield[@tag='245']/subfield[@code='a']">
				<xsl:value-of select="//datafield[@tag='245']/subfield[@code='a']"/>
			</xsl:if>
			<xsl:else>
				<xsl:value-of select="//datafield[@tag='130']/subfield[@code='a']"/>
			</xsl:else>
		</td>
		</tr>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="imprint">
		<xsl:if test="//datafield[@tag='260']">
			<tr>
			<td class="header"><xsl:text>Imprint:</xsl:text></td>
			<td>
				<xsl:for-each select="//datafield[@tag='260']">
					<xsl:value-of select="."/><br/>
				</xsl:for-each>
			</td>
			</tr>
		</xsl:if>
	</xsl:template>
     
	
	<xsl:template name="format">
		<xsl:if test="//datafield[@tag='300']">
		<tr>
		<td class="header"><xsl:text>Format:</xsl:text></td>
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
		<tr>
		<td class="header"><xsl:text>Language:</xsl:text></td>
		<td>
		 <xsl:variable name="lang">
			<xsl:value-of select="substring(//controlfield[@tag='008']/text(), 36, 3)"/>
		</xsl:variable>
		<xsl:if test="document('')/xsl:stylesheet/lang:name[@abbr=$lang]"> 
			<xsl:value-of select="document('')/xsl:stylesheet/lang:name[@abbr=$lang]"/>
		</xsl:if>
		<xsl:else>
			<xsl:value-of select="$lang"/>
		</xsl:else>
		</td>
		</tr>
	</xsl:template>
	

	<xsl:template name="istcNumber">
		<xsl:if test="//controlfield[@tag='001']">
			<tr>
				<td class="header"><xsl:text>ISTC Number:</xsl:text></td>
				<td>
					<xsl:value-of select="//controlfield[@tag='001']"/>
				</td>
			</tr>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="references">
		<xsl:if test="//datafield[@tag='510']">
			<tr>
				<td class="header"><xsl:text>References:</xsl:text></td>
				<td>
					<div style="display: block" id="abbrRefs">
					<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
						<xsl:value-of select="."/><xsl:text>; </xsl:text>
					</xsl:for-each>
					<br /><a href="javascript:expandRefs()">expand references</a>
					</div>
					<div style="display: none" id="fullRefs">
					<xsl:for-each select="//datafield[@tag='510']/subfield[@code='a']">
						<xsl:variable name="ref">
							<xsl:value-of select="substring-before(current(), ' ')"/>
						</xsl:variable>
						<strong><xsl:value-of select="."/></strong><xsl:text>: </xsl:text>
						<xsl:value-of select="document(concat('http://localhost/istc/search/?operation=references&amp;q=', $ref))/record//full"/>
						<br />
					</xsl:for-each>
					<a href="javascript:collapseRefs()">collapse references</a>
					</div>
				</td>
			</tr>
		</xsl:if>
	</xsl:template>
	

	<xsl:template name="reproductions">
		<xsl:if test="//datafield[@tag='530']">
			<tr>
				<td class="header">
					<xsl:text>Reproductions:</xsl:text>
				</td>
				<td>
					<xsl:for-each select="//datafield[@tag='530']">
						<xsl:for-each select="subfield[not(@code='u')]">
							<xsl:value-of select="." />
						</xsl:for-each>
						<br/>
						<xsl:if test="subfield[@code='u']">
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
			<tr>
				<td class="header"><xsl:text>Notes:</xsl:text></td>
				<td>
					<xsl:for-each select="//datafield[@tag='500']">
						<xsl:choose>
							<xsl:when test="contains(., $lib) and $ilc">
								<xsl:value-of select="."/><br/>
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
		</xsl:if>
	</xsl:template>


	<xsl:template name="shelfmark">
		<xsl:if test="//datafield[@tag='852']">
			<tr>
				<td class="header"><xsl:text>British Library Shelfmark:</xsl:text></td>
				<td>
					<xsl:value-of select="//datafield[@tag='852']"/>
				</td>
			</tr>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="locations">
		<xsl:if test="//datafield[@tag='951']|//datafield[@tag='995']|//datafield[@tag='957']|//datafield[@tag='997']|//datafield[@tag='954']|//datafield[@tag='955']|//datafield[@tag='996']|//datafield[@tag='952']|//datafield[@tag='958']|//datafield[@tag='953']|//datafield[@tag='994']">
			<tr>
				<td class="header"><xsl:text>Locations:</xsl:text></td><td></td>				
			</tr>
			<xsl:if test="//datafield[@tag='951']">
				<tr>
					<td align="right" class="subheader"><xsl:text>British Isles:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='951']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='995']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Belgium:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='995']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='957']">
				<tr>
					<td align="right" class="subheader"><xsl:text>France:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='957']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='997']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Germany:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='997']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='954']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Italy:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='954']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='955']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Spain/Portugal:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='955']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='996']">
				<tr>
					<td class="subheader"><xsl:text>Netherlands:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='996']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='952']">
				<tr>
					<td align="right" class="subheader"><xsl:text>U.S.A:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='952']/subfield">
					<xsl:variable name="ref">
						<xsl:value-of select="current()"/>
					</xsl:variable>			
					<xsl:value-of select="document(concat('http://localhost/istc/search/?operation=usareferences&amp;q=', $ref))/record//full"/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='958']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Other Europe:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='958']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='953']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Other:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='953']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
			<xsl:if test="//datafield[@tag='994']">
				<tr>
					<td align="right" class="subheader"><xsl:text>Doubtful:</xsl:text></td>					
				<td>
				<xsl:for-each select="//datafield[@tag='994']/subfield">
					<xsl:value-of select="."/><xsl:text>; </xsl:text>
				</xsl:for-each>
				</td>
				</tr>
			</xsl:if>
		</xsl:if>
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