/* Default Styles */
html, body {
	background: 
	margin: 0;
	font-family: Verdana, Arial, Helvetica, sans-serif;
	font-size: 90%;
	line-height: 1.1em;
}
/* End of Default Styles */


/* Text Area */
#pagecontent {
	position: absolute;
	top: 73px;
	left: 0px;
	background: #fff;
}
/* End of Text Area */


/* Hyperlinks */
a:link {	color: #214C9D; }
a:visited {	color: #214C9D; }
a:focus, a:hover, a:active {	color: #666;}
/* End of Hyperlinks */


#titlebarcontent A{
	text-decoration: none;
	color: #ffffff;
	padding: 2px;
}
#titlebarcontent A:hover{
	text-decoration: none;
	color: #ffffff;
	padding: 2px;
}
#titlebarcontent A:visited{
	text-decoration: none;
	color: #ffffff;
	padding: 2px;
}
/* End of Breadcrumb navigation */

/* Changing Content */
#subcontent {
	position: absolute;
	top: 1.6em;
	border-top: solid #000000 1px;
	left: 0px;
	width: 800px;
	voice-family: "\"}\""; 
  	voice-family:inherit;
	/*width: 790px;*/
	background: #fff ;
}
#subcontentleft{
	float: left;
	width: 620px;
	padding: 0px;
	padding-bottom: 1em;
}
#subcontentleft img{
	float: left;
	padding: 10px 10px 10px 0;
}
#subcontentleftnav{
	float: left;
	background: #b3eef8;
	width: 135px;
	max-width: 135px;
	/*height: 466px;*/
	padding: 0;
	margin: 0;
	background: url(./menu_bg2.jpg) left top repeat-y; 
}
#subcontentleftnav p {
	line-height: 1em;
}
#subcontentleftnav p a{
	border: 1px #ccc dotted;
	display: block;
	width: 125px;
	padding: 5px 2px 7px 2px;
	margin: 2px;
	background: #DAE8FF;
	color: #3C5A92;
	opacity: 85;
	filter:alpha(opacity=85);
	font-weight: bold;
	text-decoration: none;
}
#subcontentleftnav p a:hover {
	background: #3C5A92;
	color: #fff;
}
#subcontentleftcontent{
	float: right;
	width: 470px;
}
/*#subcontentleftcontent img{
	float: right;
	padding: 3px;
	border: 1px #000 solid;
	margin: 3px;
}	*/

#subcontentright img{
	float: left;
	padding: 5px 5px 10px 0;
	margin: 0;
}


#footer {
	float: none;
	width: 800px;
	border-top: 1px #216976 dotted;
	font-size: 85%;
	text-align: center;
	clear: both; 
	padding-bottom: 0.5em;
}

.newschunk {
	border: 1px #216976 dotted;
	display: block;
	padding-left: 10px;
	padding-right: 6px;
	margin-bottom: 10px;
}

.smallprint {
	font-size: 80%;
	color: #4c7a87;
}

h1 {		
	background:#415FA5;
	color:#C0D4F9;
	font-size: 140%;
	margin-top: 3em;
	padding: 10px;
	}
h2 {
	font-size: 100%;
	color: #fe9a01;
	line-height: 1em;
	margin-top: 1em;
}
h3 {
	font-size: 90%;
	color: #2e535c;
}
li {
	list-style: outside url(./bullet.gif);
	margin-left: 7px;
	margin-top: 5px;
	
}
ul {
	padding: 0 0.5em 0 0.5em;
	margin-left: 0;
}



table {
 
 	width:100%;
	
	

}

#termListTable table {

}



th {
	text-align: center;
	background:#415FA5;
	color: #fff;
	padding: 0.5em 0 0.5em 0;
}	

}
#subcontentleftcontent table {
	width: 460px;
	table-layout:fixed;
	max-width: 460px;
	font-size: 90%;
}
#subcontentleftcontent table .tablename {
	width: 180px;

}
#subcontentleftcontent table .tablecontact {
	width: 180px;

}
#subcontentleftcontent table .tableinstitute {
	width: 110px;

}
#subcontentleftcontent table hr {
	border:1px #eee dotted;

}

#searchbox {
	background: #fff;
}
#searchbox img {
	float: none;
	display: block;
}

/* added by John for easier-to-click links */
a.recslink,
a.termlink {
  padding-left: 0.8em;
  padding-right: 1em;
  margin: 1px;
  border: 1px outset black;
  min-width: 50px;
  text-decoration: none;
}

a.recslink:link, a.recslink:visited,
a.termlink:link, a.termlink:visited	
{
  background-color: #deddf4;
}	

a.termlink:hover, a.termlink:active, a.termlink:visited:hover,
a.recslink:hover, a.recslink:active, a.recslink:visited:hover
{
  background-color: #ffe2b5;
}
.navbarlayout
{
width: 15%;
vertical-align: top;
text-align: center;
}