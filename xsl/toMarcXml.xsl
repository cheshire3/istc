<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	
  <xsl:output method="xml" version="1.0" indent="yes"/>
  <xsl:preserve-space elements="*"/>	


  <xsl:template match="/">
  	<record>
  		<xsl:apply-templates/>
  	</record>
  </xsl:template>
  
  
  <xsl:template match="/usmarc/leader">
  	<leader>
  		<xsl:value-of select="lrl"/>
  		<xsl:value-of select="recstat"/>
  		<xsl:value-of select="rectype"/>
  		<xsl:value-of select="biblevel"/>
  		<xsl:value-of select="ucp"/>
  		<xsl:value-of select="indcount"/>
  		<xsl:value-of select="sfcount"/>
  		<xsl:value-of select="baseaddr"/>
  		<xsl:value-of select="enclevel"/>
  		<xsl:value-of select="dsccatfm"/>
  		<xsl:value-of select="linkrec"/>
  		<xsl:value-of select="entrymap/flength"/>
  		<xsl:value-of select="entrymap/scharpos"/>
  		<xsl:value-of select="entrymap/idlength"/>
  		<xsl:value-of select="entrymap/emucp"/>
  	</leader>
  </xsl:template>
  
  
  <xsl:template match="//fld001">
  	<controlfield tag="001">
  		<xsl:value-of select="."/>
  	</controlfield>
  </xsl:template>
  
 
  <xsl:template match="//fld008">
  	<controlfield tag="008">
  		<xsl:value-of select="."/>
  	</controlfield>
  </xsl:template>
  
  <xsl:template match="//vardflds//fld952">
  	<datafield tag="{substring-after(name(), 'fld')}" ind1="{./@*[position()=1]}" ind2="{./@*[position()=2]}">
		<xsl:variable name="usastring">
			<xsl:value-of select="a/text()"/>
		</xsl:variable>  	
		<xsl:choose>	
		<xsl:when test="contains($usastring, ' ')">
			<subfield code="a">
				<xsl:value-of select="substring-before($usastring, ' ')"/>
			</subfield>
			<subfield code="b">
				<xsl:value-of select="substring-after($usastring, ' ')"/>
			</subfield>
		</xsl:when>
		<xsl:otherwise>
			<subfield code="a">
				<xsl:value-of select="$usastring"/>
			</subfield>
		</xsl:otherwise>
		</xsl:choose>
	</datafield>
  </xsl:template>
  
  
  <xsl:template match="//vardflds//*[starts-with(name(), 'fld')]">
  	<xsl:choose>
	  	<xsl:when test="name()='fld9xx'">
	  		<xsl:apply-templates/>
	  	</xsl:when>
	  	<xsl:otherwise>
	  	<datafield tag="{substring-after(name(), 'fld')}" ind1="{./@*[position()=1]}" ind2="{./@*[position()=2]}">
	  		<xsl:for-each select="./*">
	  			<subfield code="{name()}">
	  				<xsl:value-of select="."/>
	  			</subfield>
	  		</xsl:for-each>
	  	</datafield>
	  	</xsl:otherwise>
  	</xsl:choose>
  </xsl:template>
  
  
</xsl:stylesheet>