<?xml version="1.1" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
				xmlns:lang="http://www.cheshire3.org"
				xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str">
                <!-- xmlns:c3fn="http://www.cheshire3.org/ns/xsl/" >-->


	
	 <xsl:output method="xml" omit-xml-declaration="yes" encoding="utf-8"/>
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

	 
	<xsl:template match="/">	
		<rec>
			<xsl:call-template name="contents"/>
		</rec>
	</xsl:template>

	<xsl:template name="contents">
		<xsl:call-template name="istcNumber"/>		
		<xsl:call-template name="author"/>	
		<xsl:call-template name="heading"/>
 		<xsl:call-template name="title"/>
		<xsl:call-template name="imprint"/>
		<xsl:call-template name="imprint_extra"/>
		<xsl:call-template name="format"/>
		<br/>	
		<xsl:call-template name="references"/>
		<xsl:call-template name="reproductions"/> 
		<xsl:call-template name="notes"/>
		<xsl:call-template name="locations"/>	  
			
	</xsl:template>

 	<xsl:template name="author">
 		<b>
 		<xsl:choose>
	 		<xsl:when test="//datafield[@tag='100']">
 				<xsl:choose>
					<xsl:when test="//datafield[@tag='100']/subfield[@code='a']">
						<xsl:value-of select="//datafield[@tag='100']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise test="//datafield[@tag='100']">
						<xsl:value-of select="//datafield[@tag='100']"/>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:text>. </xsl:text>
			</xsl:when>
		</xsl:choose>
		</b>
	</xsl:template>


 	<xsl:template name="heading">
 		<xsl:if test="//datafield[@tag='130']">
 		<b>
			<xsl:choose>
				<xsl:when test="//datafield[@tag='130']/subfield[@code='a']">					
					<xsl:value-of select="//datafield[@tag='130']/subfield[@code='a']" />
				</xsl:when>
				<xsl:otherwise test="//datafield[@tag='130']">
					<xsl:value-of select="//datafield[@tag='130']" />
				</xsl:otherwise>
			</xsl:choose>
			<xsl:text>. </xsl:text>
		</b>
 		</xsl:if>
 	</xsl:template>


 	<xsl:template name="title">
		<xsl:if test="//datafield[@tag='245']/subfield[@code='a']">
			<i><xsl:choose>
				<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
					<xsl:value-of select="//datafield[@tag='245']/subfield[@code='a']"/>
				</xsl:when>
			</xsl:choose>
			<xsl:text>. </xsl:text>
			</i>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="imprint">
		<xsl:if test="//datafield[@tag='260']">	
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
								<xsl:value-of select="subfield[@code='c']"/><xsl:text>. </xsl:text>
							</xsl:if>					
						</xsl:when>
					</xsl:choose>
				</xsl:for-each>
			</xsl:variable>
			<xsl:value-of select="$value"/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="imprint_extra">
		<xsl:if test="count(//datafield[@tag='260']) &gt; 1">	
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
			<xsl:value-of select="substring($value, 0, string-length($value)-5)"/>
			<xsl:text>. </xsl:text>
		</xsl:if>
	</xsl:template>    
	
	<xsl:template name="format">
		<xsl:if test="//datafield[@tag='300']/subfield">
			<xsl:value-of select="//datafield[@tag='300']/subfield"/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="istcNumber">
		<xsl:if test="//controlfield[@tag='001']">
			<xsl:value-of select="//controlfield[@tag='001']"/>		
			<br/>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="references">
		<xsl:if test="//datafield[@tag='510']">
			<xsl:variable name="value">
				<xsl:for-each select="//datafield[@tag='510']">
					<xsl:value-of select="./subfield[@code='a']"/>
					<xsl:choose>
						<xsl:when test="./subfield[@code='c']">
							<xsl:text> </xsl:text><xsl:value-of select="./subfield[@code='c']"/><xsl:text>; </xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>; </xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>			
			</xsl:variable>	
			<b><xsl:text>Refs.: </xsl:text></b>
			<xsl:value-of select="substring($value, 0, string-length($value)-1)"/>
			<br/>
		</xsl:if>
	</xsl:template>
	
	
	<xsl:template name="reproductions">
		<xsl:if test="//datafield[@tag='530']">
			<xsl:variable name="value">
				<xsl:for-each select="//datafield[@tag='530']">						
					<xsl:for-each select="subfield[not(@code='u')]">
						<xsl:value-of select="." />
					</xsl:for-each>				
					<xsl:text>; </xsl:text>												
				</xsl:for-each>				
			</xsl:variable>
			<b><xsl:text>Reproductions: </xsl:text></b>
			<xsl:value-of select="substring($value, 0, string-length($value)-1)"/>
			<br/>
		</xsl:if>
	</xsl:template>
		
	<xsl:template name="notes">
		<xsl:if test="//datafield[@tag='500']|//datafield[@tag='505']">
			<b><xsl:text>Notes: </xsl:text></b>
			<xsl:for-each select="//datafield[@tag='500']/subfield">		
				<xsl:value-of select="."/>
				<xsl:text> </xsl:text>
			</xsl:for-each>
			<xsl:for-each select="//datafield[@tag='505']/subfield">	
				<xsl:value-of select="."/>
				<xsl:text> </xsl:text>
			</xsl:for-each>
			<br/>		
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="locations">		
		<xsl:if test="(//datafield[@tag='951'] or //datafield[@tag='852'])">
			<b><xsl:text>British Isles: </xsl:text></b>
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
			<xsl:value-of select="substring($v1, 0, string-length($v1)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='995']">
			<b><xsl:text>Belgium: </xsl:text></b>
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
			<xsl:value-of select="substring($v2, 0, string-length($v2)-1)"/>
			<br/>	
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='957']">
			<b><xsl:text>France: </xsl:text></b>
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
			<xsl:value-of select="substring($v3, 0, string-length($v3)-1)"/>
			<br/>										
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='997'][not(subfield[@code='x'])]">
			<b><xsl:text>Germany: </xsl:text></b>
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
			<xsl:value-of select="substring($v4, 0, string-length($v4)-1)"/>
			<br/>			
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='954']">
			<b><xsl:text>Italy: </xsl:text></b>
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
			<xsl:value-of select="substring($v5, 0, string-length($v5)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='955']">
			<b><xsl:text>Spain/Portugal: </xsl:text></b>
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
			<xsl:value-of select="substring($v6, 0, string-length($v6)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='996']">
			<b><xsl:text>Netherlands: </xsl:text></b>
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
			<xsl:value-of select="substring($v7, 0, string-length($v7)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='993']">
			<b><xsl:text>Austria: </xsl:text></b>
			<xsl:variable name="v12">
				<xsl:for-each select="//datafield[@tag='993'][not(subfield[@code='x'])]">
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
			<xsl:value-of select="substring($v12, 0, string-length($v12)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='952']">		
			<b><xsl:text>U.S.A: </xsl:text></b>
			<xsl:variable name="v8">
				<xsl:text>%usalocs%</xsl:text>
			</xsl:variable>
			<!-- <xsl:variable name="v8">
				<xsl:for-each select="//datafield[@tag='952'][not(subfield[@code='x'])]">						
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
			</xsl:variable> -->
<!-- 			<xsl:variable name="v8">
				<xsl:for-each select="//datafield[@tag='952'][not(subfield[@code='x'])]">
					<xsl:value-of select="document('http://istc.bl.uk?)"/>
				</xsl:for-each>
				<xsl:text>%usalocs%</xsl:text>
			</xsl:variable>-->
			<xsl:value-of select="$v8"/>
			<br/>
		</xsl:if>
	
		<xsl:if test="//datafield[@tag='958']">
			<b><xsl:text>Other Europe: </xsl:text></b>
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
			<xsl:value-of select="substring($v9, 0, string-length($v9)-1)"/>
			<br/>
		</xsl:if>
			
		<xsl:if test="//datafield[@tag='953']">	
			<b><xsl:text>Other: </xsl:text></b>
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
			<xsl:value-of select="substring($v10, 0, string-length($v10)-1)"/>
			<br/>
		</xsl:if>
			
			<xsl:if test="//datafield[@tag='994']">				
				<b><xsl:text>Doubtful: </xsl:text></b>
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
				<xsl:value-of select="substring($v11, 0, string-length($v11)-1)"/>
				<br/>							
			</xsl:if>

	</xsl:template>
	

</xsl:stylesheet>