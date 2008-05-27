<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8" />
	<xsl:preserve-space elements="*" />
	
	<xsl:template match="/">
		<div id="formDiv" name="form" class="formDiv" onscroll="hideAllMenus()">
			<form id="istcForm" name="istcForm" action="#">
			
			
			<p><strong>ISTC Number:</strong><br/>
				<xsl:choose>
					<xsl:when test="//controlfield[@tag='001']">
						<xsl:apply-templates select="//controlfield[@tag='001']"/>
					</xsl:when>
					<xsl:otherwise>
						<input class="menuField" type="text" onfocus="setCurrent(this);" name="controlfield[@tag='001']" id="ISTCNo" size="10" maxlength="10"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			
			
			<p><strong>Author(s):</strong><br/>
				<xsl:choose>
					<xsl:when test="//datafield[@tag='100']|datafield[@tag='130']">
						<xsl:apply-templates select="//datafield[@tag='100']|datafield[@tag='130']"/>
					</xsl:when>
					<xsl:otherwise>
						<select name="authorsel"><option value="null">Select...</option><option value="130">Uniform Title</option><option value="100">Personal</option></select><br />
						<input class="menuField" type="text" onfocus="setCurrent(this);" onkeyup="suggest(event, this.id)" name="author" id="author" size="39"></input><br />
						
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			
			
			<p><strong>Title:</strong><br/>
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:apply-templates select="//datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<input class="menuField" type="text" onfocus="setCurrent(this);" name="datafield[@tag='245']/subfield[@code='a']" id="title" size="39"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			
			<p><strong>Imprints:</strong><br/>
			<div id="addedimprints" style="display:none" class="added"><ul id="addedimprintslist"></ul></div>
				<div id="imprintstable" class="tablecontainer">
					<table id="table_imprints"><tbody>
						<tr><td class="label">Place:</td><td> <input type="text" onkeyup="suggest(event, this.id)" onfocus="setCurrent(this);" name="imprints_a" id="imprints_a" size="36"></input><br/></td></tr>
						<tr><td class="label">Printer:</td><td> <input type="text" onkeyup="suggest(event, this.id)" onfocus="setCurrent(this);" name="imprints_b" id="imprints_b" size="36"></input><br/></td></tr>
						<tr><td class="label">Date:</td><td> <input type="text" onfocus="setCurrent(this);" name="imprints_c" id="imprints_c" size="36"></input><br/></td></tr>
						<tr><td><input class="mebutton" type="button" onclick="addEntry('imprints');" value="Add"></input></td><td></td></tr>
				    	</tbody></table>
				</div>
			</p>
			<br/>
			</form>
		</div>
	</xsl:template>
	
	
	<xsl:template match="controlfield[@tag='001']">
		<input class="menuField" type="text" readonly="true" onfocus="setCurrent(this);" name="controlfield[@tag='001']" id="ISTCNo" size="10" maxlength="10">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>			
		</input>
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='245']/subfield[@code='a']">
		<input class="menuField" type="text" onfocus="setCurrent(this);" name="datafield[@tag='245']/subfield[@code='a']" id="title" size="39">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>
		</input>
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='100']/subfield[@code='a']">
		<input class="menuField" type="text" onfocus="setCurrent(this);" onkeyup="suggest(event, this.id)" name="author" id="author" size="39">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>
		</input><br />
		<select name="authorsel"><option value="null">   </option><option value="130">Uniform Title</option><option value="100" selected="selected">Personal</option></select>
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='130']/subfield[@code='a']">
		<input class="menuField" type="text" onfocus="setCurrent(this);" name="datafield[@tag='130']/subfield[@code='a']" id="Author" size="39">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>
		</input><br />
		<select name="authorsel"><option value="null">   </option><option value="130" selected="selected">Uniform Title</option><option value="100">Personal</option></select>
	</xsl:template>
	
	
</xsl:stylesheet>