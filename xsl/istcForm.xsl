<?xml version="1.0" encoding="utf-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

	<xsl:output method="xml" omit-xml-declaration="yes" encoding="UTF-8" />
	<xsl:preserve-space elements="controlfield datafield" />
	
	<xsl:template match="/">
		<div id="formDiv" name="form" class="formDiv" onscroll="hideAllMenus()">
			<form id="mainform" name="mainform" action="#">
			<input type="hidden" id="opvalue" name="operation"/>
			<input type="hidden" id="leader" name="leader">			
				<xsl:attribute name="value">
					<xsl:value-of select="//leader"/>				
				</xsl:attribute>
			</input>
			<div class="field">
				<input type="button" onclick="submitForm('save')" value=" Save "/>
			</div>
			<div class="field">
			<p><strong>ISTC Number:</strong><br/>
				<xsl:choose>
					<xsl:when test="//controlfield[@tag='001']">
						<xsl:apply-templates select="//controlfield[@tag='001']"/>
					</xsl:when>
					<xsl:otherwise>
						<input name="1" id="ISTCNo" type="text" onfocus="setCurrent(this);" size="12" maxlength="10"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			</div>
			<br/>
			<div class="field">
			<p><strong>Author(s):</strong><br/>
				<input name="author_ind" id="author_ind" type="hidden" value="0-0"/>
				<xsl:choose>
					<xsl:when test="//datafield[@tag='100']|datafield[@tag='130']">
						<xsl:apply-templates select="//datafield[@tag='100']|datafield[@tag='130']"/>
					</xsl:when>
					<xsl:otherwise>
						<select name="author_sel"><option value="null">Select...</option><option value="130">Uniform Title</option><option value="100">Personal</option></select><br />
						<input id="author" type="text" onfocus="setCurrent(this);" onkeyup="suggestDelay(this.id, event);" autocomplete="off" name="author_a" size="99"></input><br />					
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			</div>
			<br/>
			
			<div class="field">
			<p><strong>Title:</strong><br/>
				<input name="245_ind" id="245_ind" type="hidden" value="1-0"/>
				<xsl:choose>
					<xsl:when test="//datafield[@tag='245']/subfield[@code='a']">
						<xsl:apply-templates select="//datafield[@tag='245']/subfield[@code='a']"/>
					</xsl:when>
					<xsl:otherwise>
						<textarea name="245_a" id="title" type="text" onfocus="setCurrent(this);" cols="97" rows="4"><xsl:text> </xsl:text></textarea>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			</div>
			<br/>
			<div class="field">
			<p><strong>Imprints:</strong><br/>	
				<div id="imprintstable" class="tablecontainer">
					<table id="table_imprints"><tbody>
						<tr><td class="melabel">Place:</td><td> <input type="text" onkeyup="suggestDelay(this.id, event);" autocomplete="off" onfocus="setCurrent(this);" name="imprints" id="260_a" size="36"></input><br/></td></tr>
						<tr><td class="melabel">Printer:</td><td> <input type="text" onkeyup="suggestDelay(this.id, event);" autocomplete="off" onfocus="setCurrent(this);" name="imprints" id="260_b" size="36"></input><br/></td></tr>
						<tr><td class="melabel">Date:</td><td> <input type="text" onfocus="setCurrent(this);" autocomplete="off" name="imprints" id="260_c" size="36"></input><br/></td></tr>
						<tr><td><input class="mebutton" type="button" onclick="addEntry('imprints');" value="Add"></input></td><td></td></tr>
				    </tbody></table>
				</div><br />
				<div class="addedcontainer">
					<xsl:choose>
						<xsl:when test="//datafield[@tag='260']">
							 <xsl:call-template name="accesspoint">
								<xsl:with-param name="typename" select="'imprint'"/>
								<xsl:with-param name="tagnumber" select="'260'"/>
							</xsl:call-template> 
						</xsl:when>
						<xsl:otherwise>
							<div id="addedimprints" style="display:none" class="added"><ul id="addedimprintslist"></ul></div>
						</xsl:otherwise>
					</xsl:choose>	
				</div>
			</p>
			</div>
			<br/>
			<div class="field">
			<p><strong>Format:</strong><br/>
				<input name="300_ind" id="300_ind" type="hidden" value="0-0"/>
				<xsl:choose>
					<xsl:when test="//datafield[@tag='300']">
						<xsl:apply-templates select="//datafield[@tag='300']"/>
					</xsl:when>
					<xsl:otherwise>
						<input name="300_c" id="format" type="text" onfocus="setCurrent(this);" size="39"></input>
					</xsl:otherwise>
				</xsl:choose>      
			</p>
			</div>
			<br/>
			<div class="field">
			<p><strong>008 Field</strong></p>
			<xsl:choose>
				<xsl:when test="//controlfield[@tag='008']">
					<xsl:apply-templates select="//controlfield[@tag='008']"/>
				</xsl:when>
				<xsl:otherwise>
					<div class="horizontal"><p>
						<strong>Date Type:</strong><br/>
						<select name="8_datetype"><option value=" ">Select...</option><option value="s">Single Date</option><option value="b">No Dates Given</option><option value="m">Beginning/End Dates</option></select><br />
					</p></div>
					<div class="horizontal"><p>
						<strong>Original:</strong><br/>
						<input name="8_original" type="text" size="8" maxlength="6" value="      "> </input>
					</p></div>
					<div class="horizontal"><p>
						<strong>Date 1:</strong><br/>
						<input name="8_date1" type="text" size="6" maxlength="4" value="    "> </input>
					</p></div>
					<div class="horizontal"><p>
						<strong>Date 2:</strong><br/>
						<input name="8_date2" type="text" size="6" maxlength="4" value="    "> </input>
					</p></div>
					<div class="horizontal"><p>
						<strong>Language:</strong><br/>
						<input name="8_lang" type="text" size="7" maxlength="3" value="   "></input>
					</p></div>
				</xsl:otherwise>
			</xsl:choose>
			</div>
			<br/>
			<div class="field">
			<p><strong>General Note:</strong><br/>		
				<div id="generalnotestable" class="tablecontainer">
					<table id="table_generalnotes"><tbody>
						<tr><!-- <td class="melabel"></td> --><td> <textarea onfocus="setCurrent(this);" name="generalnotes" id="500_a" cols="97" rows="4"><xsl:text> </xsl:text></textarea><br/></td></tr>
						<tr><td><input class="mebutton" type="button" onclick="addEntry('generalnotes');" value="Add"></input></td><td></td></tr>
				    </tbody></table>
				</div><br />
				<div class="addedcontainer">
					<xsl:choose>
						<xsl:when test="//datafield[@tag='500']">
							 <xsl:call-template name="accesspoint">
								<xsl:with-param name="typename" select="'generalnote'"/>
								<xsl:with-param name="tagnumber" select="'500'"/>
							</xsl:call-template> 
						</xsl:when>
						<xsl:otherwise>
							<div id="addedgeneralnotes" style="display:none" class="added"><ul id="addedgeneralnoteslist"></ul></div>
						</xsl:otherwise>
					</xsl:choose>
				</div>
			</p>
			</div>
			<br/>
		 	<div class="field">
			<p>
				<div id="refcontainer"><strong>References:</strong><br/>				
					<div id="referencestable" class="tablecontainer">
						<table id="table_references"><tbody>
							<tr><td class="melabel">Reference:</td><td> <input type="text" onfocus="setCurrent(this);" onkeyup="suggest(this.id, event);" autocomplete="off" name="references" id="510_a" size="30"></input><br/></td></tr>
					   		<tr><td class="melabel">Other Details:</td><td> <input type="text" onfocus="setCurrent(this);" name="refpages" id="510_other" size="30"  autocomplete="off" /></td></tr>
					    	<tr></tr>
					    </tbody></table>
					</div>
				</div>
				<div id="fullrefcontainer" class="reflabel">					
					<div id="reflabel">
					<strong>Full Reference:</strong>
					</div>
				    <div id="refdisplay">
						<p></p>
					</div>
				</div>
				<br />
				<div>					
					<input type="button" onclick="addEntry('references');" value="Add"/>
					<input type="button" onclick="editRef();" value="edit/create ref"/>
				</div><br />
				
			<!-- <div class="meadded"> -->	
				<div class="addedcontainer">
					<xsl:choose>
						<xsl:when test="//datafield[@tag='510']">
							<xsl:text>%RFRNC%</xsl:text>
							<!-- <xsl:call-template name="accesspoint">
								<xsl:with-param name="typename" select="'reference'"/>
								<xsl:with-param name="tagnumber" select="'510'"/>
							</xsl:call-template> -->
						</xsl:when>
						<xsl:otherwise>
							<div id="addedreferences" style="display:none" class="added"><ul id="addedreferenceslist"></ul></div>
						</xsl:otherwise>
					</xsl:choose>	
				</div>	
			</p>
			</div> 
			<br/>
			<div class="field">
			<p><strong>Reproductions Notes:</strong><br/>
					
				<div id="repnotestable" class="tablecontainer">
					<table id="table_repnotes"><tbody>
						<tr><td class="melabel">Note:</td><td> <textarea onfocus="setCurrent(this);" name="repnotes" id="530_a" cols="89" rows="4"><xsl:text> </xsl:text></textarea><br/></td></tr>
						<tr><td class="melabel">URL:</td><td> <textarea onfocus="setCurrent(this);" name="repnotes" id="530_u" cols="89" rows="1"><xsl:text> </xsl:text></textarea><br/></td></tr>
						<tr><td><input class="mebutton" type="button" onclick="addEntry('repnotes');" value="Add"></input></td><td></td></tr>
				    </tbody></table>
				</div><br />
				<div class="addedcontainer">
					<xsl:choose>
						<xsl:when test="//datafield[@tag='530']">
							 <xsl:call-template name="accesspoint">
								<xsl:with-param name="typename" select="'repnote'"/>
								<xsl:with-param name="tagnumber" select="'530'"/>
							</xsl:call-template> 
						</xsl:when>
						<xsl:otherwise>
							<div id="addedrepnotes" style="display:none" class="added"><ul id="addedrepnoteslist"></ul></div>
						</xsl:otherwise>
					</xsl:choose>	
				</div>
			</p>
			</div>
			<br/>
			<div class="field">
			<p><strong>British Library Shelfmark:</strong><br/>
				<div id="blshelfmarkstable" class="tablecontainer">
					<table id="table_blshelfmarks"><tbody>
						<tr><td class="melabel">Place:</td><td> <input type="text" onfocus="setCurrent(this);" name="blshelfmarks" id="852_a" size="36" value="British Library"></input></td></tr>
						<tr><td class="melabel">Note:</td><td> <input type="text" onfocus="setCurrent(this);" name="blshelfmarks" id="852_q" size="36"></input></td></tr>
						<tr><td class="melabel">Shelfmark:</td><td> <input type="text" onfocus="setCurrent(this);" name="blshelfmarks" id="852_j" size="36"></input></td></tr>
						<tr><td><input class="mebutton" type="button" onclick="addEntry('blshelfmarks');" value="Add"></input></td><td></td></tr>
				    </tbody></table>
				</div><br />
				<div class="addedcontainer">
					<xsl:choose>
						<xsl:when test="//datafield[@tag='852']">
							 <xsl:call-template name="accesspoint">
								<xsl:with-param name="typename" select="'blshelfmark'"/>
								<xsl:with-param name="tagnumber" select="'852'"/>
							</xsl:call-template> 
						</xsl:when>
						<xsl:otherwise>
							<div id="addedblshelfmarks" style="display:none" class="added"><ul id="addedblshelfmarkslist"></ul></div>
						</xsl:otherwise>
					</xsl:choose>	
				</div>
			</p>
			</div>
			</form>
		</div>
	</xsl:template>
	
	
	<xsl:template match="controlfield[@tag='001']">
		<input name="1" id="ISTCNo" type="text" readonly="true" onfocus="setCurrent(this);" size="12" maxlength="10">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>			
		</input>
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='245']/subfield[@code='a']">
		<textarea name="245_a" id="title"  onfocus="setCurrent(this);" cols="97" rows="4">			
				<xsl:value-of select="."/>			
		</textarea>
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='100']/subfield[@code='a']">
		<select name="author_sel"><option value="null">Select...</option><option value="130">Uniform Title</option><option value="100" selected="selected">Personal</option></select><br/>
		<input type="text" onfocus="setCurrent(this);" onkeyup="suggest(event, this.id)" name="author_a" id="author_a" size="99">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>
		</input><br />
	</xsl:template>
	
	
	<xsl:template match="datafield[@tag='130']/subfield[@code='a']">
		<select name="author_sel"><option value="null">Select...</option><option value="130" selected="selected">Uniform Title</option><option value="100">Personal</option></select><br/>
		<input type="text" onfocus="setCurrent(this);" name="author_a" id="author_a" size="39">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>
		</input><br />
	</xsl:template>
	
	<xsl:template match="datafield[@tag='300']/subfield[@code='c']">
		<input type="text" onfocus="setCurrent(this);" name="300_c" id="format" size="39">
			<xsl:attribute name="value">
				<xsl:value-of select="."/>
			</xsl:attribute>			
		</input>
	</xsl:template>
	
	<xsl:template match="controlfield[@tag='008']">
		<xsl:variable name="f008">
			<xsl:value-of select="."/>
		</xsl:variable>
		<div class="horizontal"><p>
			<strong>Date Type: </strong><br/>
			<select name="8_datetype"><option value=" ">Select...</option><option value="s">Single Date</option><option value="b">No Dates Given</option><option value="m">Beginning/End Dates</option></select><br />
		</p></div>
		<div class="horizontal"><p>
			<strong>Original:</strong><br/>
			<input name="8_original" type="text" size="8" maxlength="6">
				<xsl:attribute name="value">
					<xsl:value-of select="substring($f008, 1, 6)"/>
				</xsl:attribute>
			</input>
		</p></div>
		<div class="horizontal"><p>
			<strong>Date 1:</strong><br/>
			<input name="8_date1" type="text" size="6" maxlength="4">
				<xsl:attribute name="value">
					<xsl:value-of select="substring($f008, 8, 4)"/>
				</xsl:attribute>
			</input>
		</p></div>
		<div class="horizontal"><p>
			<strong>Date 2:</strong><br/>
			<input name="8_date2" type="text" size="6" maxlength="4">
				<xsl:attribute name="value">
					<xsl:value-of select="substring($f008, 12, 4)"/>
				</xsl:attribute>
			</input>
		</p></div>
		<div class="horizontal"><p>
			<strong>Language:</strong><br/>
			<input name="8_lang" type="text" size="7" maxlength="3">
				<xsl:attribute name="value">
					<xsl:value-of select="substring($f008, 36, 3)"/>
				</xsl:attribute>
			</input>
		</p></div>
	</xsl:template>
	
 	  <xsl:template name="accesspoint">
		  	<xsl:param name="typename"/>
		  	<xsl:param name="tagnumber"/>
		  	<div style="display:block" class="added"> 
			  	<xsl:attribute name="id">
			  		<xsl:text>added</xsl:text><xsl:value-of select="$typename"/><xsl:text>s</xsl:text>
			  	</xsl:attribute>
			  	<ul>
			  		 <xsl:attribute name="id">
				  		<xsl:text>added</xsl:text><xsl:value-of select="$typename"/><xsl:text>slist</xsl:text>
				  	</xsl:attribute>
					<xsl:for-each select="//datafield[@tag = $tagnumber]">
						<li>
							<xsl:attribute name="id">
								<xsl:text>li</xsl:text><xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/>				
							</xsl:attribute>	
					  	 	<div>
								<xsl:attribute name="id">
									<xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/>				
								</xsl:attribute>			
								<div class="icons">
								<!-- delete -->
									<a>
										<xsl:attribute name="onclick">
											<xsl:text>deleteEntry('</xsl:text><xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/><xsl:text>');</xsl:text>
										</xsl:attribute>
										<xsl:attribute name="title">
											<xsl:text>delete entry</xsl:text>
										</xsl:attribute>
										<img src="/istc/images/remove.png" onmouseover="this.src='/istc/images/remove-hover.png';" onmouseout="this.src='/istc/images/remove.png';">
											<xsl:attribute name="class">
												<xsl:text>addedimage</xsl:text>
											</xsl:attribute>
										</img>
									</a>	
								<!-- Up -->
									<a>
										<xsl:attribute name="onclick">
											<xsl:text>entryUp('</xsl:text><xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/><xsl:text>');</xsl:text>
										</xsl:attribute>
										<xsl:attribute name="title">
											<xsl:text>move up</xsl:text>
										</xsl:attribute>
										<img src="/istc/images/up.png" onmouseover="this.src='/istc/images/up-hover.png';" onmouseout="this.src='/istc/images/up.png';">	
											<xsl:attribute name="class">
												<xsl:text>addedimage</xsl:text>
											</xsl:attribute>
										</img>
									</a>	
								<!-- Down -->
									<a>
										<xsl:attribute name="onclick">
											<xsl:text>entryDown('</xsl:text><xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/><xsl:text>');</xsl:text>
										</xsl:attribute>
										<xsl:attribute name="title">
											<xsl:text>move down</xsl:text>
										</xsl:attribute>
										<img src="/istc/images/down.png" onmouseover="this.src='/istc/images/down-hover.png';" onmouseout="this.src='/istc/images/down.png';">
											<xsl:attribute name="class">
												<xsl:text>addedimage</xsl:text>
											</xsl:attribute>										
										</img>
									</a>									
								</div>
								<div class="multipleEntry">	
								<p class="float">
									<xsl:attribute name="onclick">
										<xsl:text>editEntry('</xsl:text><xsl:value-of select="$typename"/><xsl:text>s_formgen', </xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/><xsl:text>);</xsl:text>
									</xsl:attribute>
									<xsl:attribute name="title">
										<xsl:text>Click to edit</xsl:text>
									</xsl:attribute>		 
									<xsl:call-template name="accesspointstring">					
										<xsl:with-param name="typename" select="$typename"/>
										<xsl:with-param name="separater" select="' '"/>
									</xsl:call-template>
								</p>
								</div>
							</div>												
							<input type="hidden">
								<xsl:attribute name="id">
									<xsl:value-of select="$typename"/><xsl:text>s_formgen</xsl:text><xsl:number level="single" count="//datafield[@tag = $tagnumber]" format="1"/><xsl:text>xml</xsl:text>
								</xsl:attribute>
								<xsl:attribute name="name">
									<xsl:value-of select="$typename"/><xsl:text>s</xsl:text>
								</xsl:attribute>
								<xsl:attribute name="value">
									<div class="accesspoint">					 
										<xsl:call-template name="accesspointstring">					
											<xsl:with-param name="tagnumber" select="$tagnumber"/>
											<xsl:with-param name="separater" select="' ||| '"/>
										</xsl:call-template>
									</div>
								</xsl:attribute>
							</input>	
						</li>		
				 	</xsl:for-each>	 	
			 	</ul>										
			</div>	  	
		  </xsl:template>
	
	
	<xsl:template name="accesspointstring">
	  	 <xsl:param name="tagnumber"/>
	  	 <xsl:param name="separater"/>
	  	 <xsl:choose>
	  	 	<xsl:when test="$separater = ' '">
	  	 		<xsl:for-each select="subfield">
	  	 			<xsl:value-of select="."/>
	  	 			<xsl:value-of select="$separater"/>
	  	 		</xsl:for-each>
	  	 	</xsl:when>
	  	 	<xsl:when test="$separater = ' ||| '">
	  	 		<xsl:for-each select="subfield">
	  	 			<xsl:value-of select="$tagnumber"/>
	  	 			<xsl:text>_</xsl:text>
	  	 			<xsl:value-of select="@code"/>
	  	 			<xsl:text> | </xsl:text>
	  	 			<xsl:value-of select="."/>
	  	 			<xsl:value-of select="$separater"/>
	  	 		</xsl:for-each>
	  	 		<xsl:choose>
	  	 			<xsl:when test="$tagnumber='100' or $tagnumber='245' or $tagnumber='959'">
	  	 				<xsl:value-of select="$tagnumber"/>
	  	 				<xsl:text>_ind | 1-0</xsl:text>
	  	 				<xsl:value-of select="$separater"/>
	  	 			</xsl:when>
	  	 			<xsl:when test="$tagnumber='510'">
	  	 				<xsl:value-of select="$tagnumber"/>
	  	 				<xsl:text>_ind | 4-0</xsl:text>
	  	 				<xsl:value-of select="$separater"/>
	  	 			</xsl:when>
	  	 			<xsl:otherwise>
	  	 				<xsl:value-of select="$tagnumber"/>
	  	 				<xsl:text>_ind | 0-0</xsl:text>
	  	 				<xsl:value-of select="$separater"/> 				
	  	 			</xsl:otherwise>
	  	 		</xsl:choose>
	  	 	</xsl:when>
	  	 </xsl:choose>
	</xsl:template> 
	
	
</xsl:stylesheet>