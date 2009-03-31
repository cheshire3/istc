/*
// Program:   istcedit.js
// Version:   0.01
// Description:
//            JavaScript functions used in the Cheshire3 ISTC editing interface 
//            
//
// Language:  JavaScript
// Author:    Catherine Smith <catherine.smith@liv.ac.uk>
// Date:      18/02/2009
//
// Copyright: &copy; University of Liverpool 2009
//
// Version History:
// 0.01 - 18/02/2009 - CS - Basic functions for edit interfaces
*/ 

var timeout;

function goto(){

	var select = document.getElementById('goto');
	var value = select.value;
	if (value != 'null') {
		location.href = '#' + value;
	}
	var select = document.getElementById('goto').selectedIndex = 0;
}

function confirmDelete(type){
	var valid = false;
	if (type == 'text'){
		var input = document.getElementById('ISTCNo');
		if (input.value.strip() != ''){
			valid = true;
		}
		if (input.value.length != 10){
			alert('The ISTC number you have entered does not contain the correct number of characters. Please check and try again');
			return false;
		}
	}
	else {
		var div = document.getElementById('colcontainer');
		if (div){
			var checkboxes = div.getElementsByTagName('input');
			for (var i=0; i<checkboxes.length; i++){
				if (checkboxes[i].checked){
					valid = true;
					break;
				}
			}
		}
	}
	if (valid){	
		switch(op) {
			case 'unindex':
				var msg = 'This operation will PERMANENTLY remove the file from the hard-disk. The record will also be removed from all indexes and will not be available for searching. Are you sure you wish to continue?';
				break;
			case 'delete':
				var msg = 'This operation will PERMANENTLY remove the file from the hard-disk. It will still be available foe searching until the database is next rebuilt. Are you sure you wish to continue?';
				break;	
			default:
				if (arguments.length == 1){
					/*hopefully a message we should send*/
					var msg = arguments[0];
				}
				break;
		}	
	}
	else {
		if (type == 'text'){
			alert('Please enter ISTC Number first');
		}
		else {
			alert('Please select records first');
		}
		return false;
	}		
	if (msg) {
		if (window.confirm) { return window.confirm(msg); }
		else if (confirm) { return confirm(msg); }
		else { return true; } // no mechanism for confirmation supported by browser - go ahead anyway
	} else {return true; } // no requirement for confirmation	
}


function checkIds(type){
	var valid = false;
	var id;
	if (type == 'text'){
		var input = document.getElementById('ISTCNo');
		if (input.value.strip() != ''){
			id = input.value.strip();
			valid = true;
		}
		if (!validate_ISTCNo(input.value.strip())){
			alert('The ISTC number you have entered is not valid. It should contain two letters followed by eight numbers');
			return false;
		}
	}
	else if (type == 'private'){
		var div = document.getElementById('privatecontainer');
		if (div){
			var checkboxes = div.getElementsByTagName('input');
			for (var i=0; i<checkboxes.length; i++){
				if (checkboxes[i].checked){
					id = checkboxes[i].value;
					valid = true;
					break;
				}
			}
			if (!valid){
				alert('Please select a record to edit');
				return false;
			}
		}
	}
	else {
		var div = document.getElementById('colcontainer');
		if (div){
			var checkboxes = div.getElementsByTagName('input');
			for (var i=0; i<checkboxes.length; i++){
				if (checkboxes[i].checked){
					id = checkboxes[i].value;
					valid = true;
					break;
				}
			}
			if (!valid){
				alert('Please select a record to edit');
				return false;
			}
		}
	}
	if (valid){
		var url = '../edit/';
		var data = 'operation=checkStore&id=' + id;
		var error = false;
		var conflict = '';
		var owner = '';
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var response = transport.responseText;
			if (response.substring(0, 4) == "<!--"){
				error = true;
			}			
			conflict = response.substring(response.indexOf('<value>')+7, response.indexOf('</value>'));
			if (response.indexOf('<owner>') > -1){
				owner = response.substring(response.indexOf('<owner>')+7, response.indexOf('</owner>'));
			}
		}});
		if (conflict == 'true'){
			if (owner == 'user'){
				alert('You already have a draft version of this file in the draft store. If you want to edit the current draft you need to open it from the draft store. If you want to edit the version from the main database you need to first delete the version from the draft store.');
				return false;
			}
			else {
				alert(owner + ' has a draft version of this file in the draft store. You will not be able to edit this file until the other user submits or discards their draft.');				
				return false;
			}
		}
		else {
			return true;
		}
		
		
		
	} else return false;

}


function checkUserInfo(){
	var userid = document.getElementById('userid').value;
	if (userid.strip() == ''){
		return false;
	}
	else {
		return true;
	}
	
}



//================================================================================================
//Functions for multiple entry fields

var nameCount = 0;

var indicators = new Array();
		indicators['100'] = '1-0';
		indicators['245'] = '1-0';
		indicators['510'] = '4-0';
		indicators['959'] = '1-0';


function validEntry(s){
	if (s == 'imprints'){
		if (document.getElementById('260_a').value.strip() == '' && document.getElementById('260_b').value.strip() == '' && document.getElementById('260_c').value.strip() == ''){
			return false;
		}
	}
	if (s == 'generalnotes'){
		if (document.getElementById('500_a').value.strip() == ''){
			return false;
		}
	}
	if (s == 'references'){
		if (document.getElementById('510_a').value.strip() == ''){
			return false;
		}	
	}
	if (s == 'repnotes'){
		if (document.getElementById('530_a').value.strip() == ''){
			return false;
		}	
	}	
	if (s == 'holdings'){
		if (document.getElementById('holdings_a').value.strip() == ''){
			return false;
		}
	}
	if (s == 'blshelfmarks'){
		if (document.getElementById('852_a').value.strip() == '' || document.getElementById('852_j[1]').value.strip() == ''){
			return false;
		}
	}	
	return true;
}


function addEntry(s){

	if (!validEntry(s)){
		return;
	}
   	var fm = document.getElementById('istcForm');
	var tableDiv = ($(s + 'table'));
	
    /* retreive all values from section of form and reset form values*/
    var valueString = '';
    var textString = '';  
	var table = tableDiv.getElementsByTagName('tbody')[0];
	var rows = table.getElementsByTagName('tr');
	var length = rows.length-1;
    for (var i = 0; i<length; i++){   
    	var textbox = rows[i].getElementsByTagName('input')[0];
    	  
    	if (textbox == null){
    		textbox = rows[i].getElementsByTagName('textarea')[0];
    	}	
    	if (textbox == null){
    		textbox = rows[i].getElementsByTagName('select')[0];
    	}
    	if (textbox.value.strip() != '' && textbox.value.strip() != ' '){
    		
    		if (s == 'holdings' && i == 0){
    			textString += textbox.value + ' - ';
    			valueString += textbox.id + ' | ' + textbox.value + ' ||| '; 
    			textbox.value = '';
    		}
    		else if (s == 'holdings' && i == 3){
    			if (textbox.checked == true){
    				valueString += textbox.id + ' | Private ||| ';
    				textString += ' - Private'; 
    				textbox.checked = false;
    			}  			
    		}
    		else {    		
    			textString += textbox.value + ' ';  
    			valueString += textbox.id + ' | ' + textbox.value + ' ||| ';
    			textbox.value = '';	    			
    		}
    		
    	}   
    	
    }
    var tag = textbox.id.split('_')[0];
    var indicatorValue = '0-0';
    if (indicators[tag]) {
    	indicatorValue = indicators[tag];
    }
    	
    valueString += tag + '_ind | ' + indicatorValue + ' ||| ';
    /* add to DOM */
    var div = document.getElementById('added' + s.toLowerCase());
    var list = document.getElementById('added' + s.toLowerCase() + 'list');
    var item = document.createElement('li');
    item.setAttribute('id', 'li' + s + nameCount);
    var txtnode = document.createTextNode(textString); 
	var number = nameCount;
    nameDiv = document.createElement('div');
    nameDiv.setAttribute('class', 'multipleEntry');
    
    p = document.createElement('p');
    a = document.createElement('a');
    a.onclick = function () {editEntry(s, number); };
     
	if (s == 'references' && document.getElementById('refdisplay').childNodes[0].firstChild){
		if (document.getElementById('refdisplay').childNodes[0].firstChild.nodeValue.strip() != ''){
			var title = document.getElementById('refdisplay').childNodes[0].firstChild.nodeValue;
		}
		else {
			var title = 'Click to edit';
		}
	}
	else {
		var title = 'Click to edit';
	}
    p.setAttribute('title', title);
    p.className = 'addedString';
    a.appendChild(txtnode);
    p.appendChild(a);
    nameDiv.appendChild(p);
    
    var icondiv = createIcons(s);

    var wrapper = document.createElement('div');
    wrapper.setAttribute('id', s + nameCount);  
    wrapper.appendChild(icondiv);
    wrapper.appendChild(nameDiv);   
    item.appendChild(wrapper);
  
    var hidden = document.createElement('input');
    hidden.setAttribute('type', 'hidden');
    hidden.setAttribute('name', s);
    hidden.setAttribute('id', s + nameCount + 'xml'); 
    hidden.setAttribute('value', valueString);

    item.appendChild(hidden);

    var ph = document.getElementById('placeholder' + s);

    if (ph != null){
    	list.replaceChild(item, ph);
    }
    else {
    	list.appendChild(item);
    }   
    if (div.style.display = 'none'){
    	div.style.display = 'block';
    }
    nameCount++;   	 
	clearRef();
	clearUsa();
	if (s == 'holdings'){
		document.getElementById('holdings_country').selectedIndex = 0;
	}
	if (s == 'blshelfmarks'){
		resetShelfmarks();
	}
}


function createIcons(s){
   var icondiv = document.createElement('div');
   icondiv.className = 'icons'; 

   var d = "'" + s + nameCount + "'";
   var s = "'" + s + "'";
   /* the delete icon */
   var innerHTMLString = '<a onclick ="deleteEntry(' + d + ');" class="addedimage" title="delete entry"><img src = "/istc/images/remove.png" onmouseover="this.src=\'/istc/images/remove-hover.png\';" onmouseout="this.src=\'/istc/images/remove.png\';"/></a>'; 
   innerHTMLString += '<a onclick ="entryUp(' + d + ');" class="addedimage" title="move up"><img src = "/istc/images/up.png" onmouseover="this.src=\'/istc/images/up-hover.png\';" onmouseout="this.src=\'/istc/images/up.png\';"/></a>';
   innerHTMLString += '<a onclick ="entryDown(' + d + ');" class="addedimage" title="move down"><img src = "/istc/images/down.png" onmouseover="this.src=\'/istc/images/down-hover.png\';" onmouseout="this.src=\'/istc/images/down.png\';"/></a>';
   innerHTMLString += '<a onclick ="insertAbove(' + s + ',' + nameCount + ');" class="addedimage" title="insert above"><img src = "/istc/images/insert.png" onmouseover="this.src=\'/istc/images/insert-hover.png\';" onmouseout="this.src=\'/istc/images/insert.png\';"/></a>';
   
   icondiv.innerHTML = innerHTMLString;
   return icondiv;
}


function entryUp(d){

	var item = document.getElementById('li' + d);
	var parent = item.parentNode;
	var listItems = parent.getElementsByTagName('li');
	var index = 0;
	for (var i=0; i<listItems.length; i++){
		if (listItems[i] == item){
			index = i;
		}
	}	
	if (index-1 >= 0){	
		item.getElementsByTagName('img')[1].src = '/istc/images/up.png';
		parent.removeChild(listItems[index]);
		parent.insertBefore(item, listItems[index-1]);
	}
}


function entryDown(d){
	var item = document.getElementById('li' + d);
	var parent = item.parentNode;
	var listItems = parent.getElementsByTagName('li');
	var index = 0;
	for (var i=0; i<listItems.length; i++){
		if (listItems[i] == item){
			index = i;
		}
	}	
	if (index+1 < listItems.length){
		item.getElementsByTagName('img')[2].src = '/istc/images/down.png';
		parent.removeChild(listItems[index]);
		parent.insertBefore(item, listItems[index+1]);
	}
}


/*deletes element with given id */
function deleteEntry(d){
  	var item = document.getElementById('li' + d);
  	var list = item.parentNode;
	list.removeChild(item);
  	if (list.getElementsByTagName('li').length < 1){
  		list.parentNode.style.display = 'none';
  	}
}


function insertAbove(s, number){

	var type = s.substring(0, s.indexOf('_formgen'));
  	if (type == '') {
  		type = s;
  	}  

 	var ph = document.getElementById('placeholder' + type);

	if (ph != null){
		var ul = ph.parentNode;
		ul.removeChild(ph);
	}

  	var item = document.getElementById('li' + s + number);
  	
  	var parent = item.parentNode;
  	
	var placeholder = document.createElement('li');
	placeholder.setAttribute('id', 'placeholder' + type);
	var image = document.createElement('img');
	image.setAttribute('src', '/istc/images/placeholder.png');
	image.className = "addedimage";
	placeholder.appendChild(image);
	parent.insertBefore(placeholder, item);
}


function resetShelfmarks(){	
	var table = document.getElementById('table_blshelfmarks');
	var tbody = table.getElementsByTagName('tbody')[0];
	var tds = tbody.childNodes;
	for (var i=tds.length-2; i>2; i--){
		tbody.removeChild(tds[i]);
	}	
}


/* repopulate the access point with the details from the given entry so they can be edited, s is either the name of the access point or the name of the access point
followed by '_formgen' which is used to maintain distinct ids between access points read in from existing xml and those created in the current form,
number is the number which forms part of the unique id */
function editEntry(s, number){
	clearUsa();
	var type = s.substring(0, s.indexOf('_formgen'));
  	if (type == '') {
  		type = s;
  	}  
  	if (type.match(/\d{3}\D*/)){
  		type = type.substring(3);
  	}
 
 	var ph = document.getElementById('placeholder' + type);
	if (ph != null){
		var ul = ph.parentNode;
		ul.removeChild(ph);
	}
  
  	var string = document.getElementById(s + number + 'xml').value;
  	var values = string.split(' ||| ');
 	var tableDiv = ($(type + 'table'));

  	var table = tableDiv.getElementsByTagName('tbody')[0];
  	var rows = table.getElementsByTagName('tr');
  	var inputs = table.getElementsByTagName('input');
  	var usa = false;
	if (type == 'holdings'){
	  	for (var i = 0; i< values.length-2; i++){ 
	  		value = values[i].split(' | ');
	  		if (i == 0) {
	  			var select = document.getElementById('holdings' + value[0].substring(value[0].indexOf('_')));
	  			for (var j = 0; j< select.length; j++){  
	  				if(select[j].value == value[1]){
     					select.selectedIndex = j;
   					}
	  			}
	  			if (value[1] == '952'){
	  				usa = true;
	  			}
	  		}
	  		else if (value[0] == 'holdings_x'){
	  			if (value[1] == 'Private'){
	  				document.getElementById('holdings_x').checked = true;
	  				document.getElementById('holdings_x').value = 'on';
	  			}
	  		}
	  		else {	
	  			document.getElementById('holdings' + value[0].substring(value[0].indexOf('_'))).value = value[1];
	  			if (usa && i==1){
	  				showUsa(value[1]);
	  			}		
	  				  				  		
	  		}
	  	}
  	} else if (type == 'blshelfmarks'){
  		resetShelfmarks();
  		for (var i = 0; i< values.length-2; i++){  
	  		value = values[i].split(' | ');
	  		if (value[0].match(/852_j\S*/)){
	  			try {
	  				document.getElementById(value[0]).value = value[1];
	  			}
	  			catch (err){
	  				var row = document.createElement('tr');
					var cell1 = document.createElement('td');
					cell1.className = 'melabel';
					cell1.appendChild(document.createTextNode('Shelfmark:'));
					row.appendChild(cell1);
					
					var cell2 = document.createElement('td');
					var input = document.createElement('input');
					input.setAttribute('size', '36');
					input.setAttribute('type', 'text');
					input.setAttribute('autocomplete', 'off');
					input.setAttribute('name', 'blshelfmarks');
					input.setAttribute('id', value[0]);
					input.setAttribute('value', value[1]);
					cell2.appendChild(input);
					row.appendChild(cell2);
					
					var cell3 = document.createElement('td');
					var image = document.createElement('img');
					image.setAttribute('src', '/istc/images/remove.png');
					image.onmouseover = function() {this.src='/istc/images/remove-hover.png';};
					image.onmouseout = function() {this.src='/istc/images/remove.png';};
					image.onclick = function() {deleteShelfmark(value[0])}
					cell3.appendChild(image);
					row.appendChild(cell3);
					
					var buttonrow = document.getElementById('buttonrow');
					table.insertBefore(row, buttonrow);	  				
	  			}
	  		}
	  		else {
	  			document.getElementById(value[0]).value = value[1];
	  		}
	  	}
  	
  	
  	}
  	else {
	  	if (inputs.length == 1){	
	  		inputs = table.getElementsByTagName('textarea');
			for (var i = 0; i< values.length-2; i++){  
		  		value = values[i].split(' | ');
		  		document.getElementById(value[0]).value = value[1];
		  	}  		
	  	}
	  	else {
		  	// replace values in order
		  	for (var i = 0; i< values.length-2; i++){  
		  		value = values[i].split(' | ');
		  		document.getElementById(value[0]).value = value[1];
		  	}
		}
		if (type == 'references'){
	  		showValue(values[0].split(' | ')[1]);
	  	}
	}
  	//delete the access point you are now editing and use placeholder if appropriate
  	var item = document.getElementById('li' + s + number);
  	var parent = item.parentNode;
	var listItems = parent.getElementsByTagName('li');
	var index = 0;
	for (var i=0; i<listItems.length; i++){
		if (listItems[i] == item){
			index = i;
		}
	}
	
	if (listItems.length > 1){
		var placeholder = document.createElement('li');
		placeholder.setAttribute('id', 'placeholder' + type);
		var image = document.createElement('img');
		image.setAttribute('src', '/istc/images/placeholder.png');
		image.className = "addedimage";
		placeholder.appendChild(image);
		parent.replaceChild(placeholder, item);
	}
	else {
		deleteEntry(s + number);
	} 	
}


function addShelfmark(){
	var table = document.getElementById('table_blshelfmarks');
	var tbody = table.getElementsByTagName('tbody')[0];
	var count = tbody.childNodes.length -2;
	
	var row = document.createElement('tr');
	var cell1 = document.createElement('td');
	cell1.className = 'melabel';
	cell1.appendChild(document.createTextNode('Shelfmark:'));
	row.appendChild(cell1);
	
	var cell2 = document.createElement('td');
	var input = document.createElement('input');
	input.setAttribute('size', '36');
	input.setAttribute('type', 'text');
	input.setAttribute('autocomplete', 'off');
	input.setAttribute('name', 'blshelfmarks');
	input.setAttribute('id', '852_j[' + count + ']');
	cell2.appendChild(input);
	row.appendChild(cell2);
	
	var cell3 = document.createElement('td');
	var image = document.createElement('img');
	image.setAttribute('src', '/istc/images/remove.png');
	image.onmouseover = function() {this.src='/istc/images/remove-hover.png';};
	image.onmouseout = function() {this.src='/istc/images/remove.png';};
	image.onclick = function() {deleteShelfmark('852_j[' + count + ']')}
	cell3.appendChild(image);
	row.appendChild(cell3);
	
	var buttonrow = document.getElementById('buttonrow');
	tbody.insertBefore(row, buttonrow);
}

function deleteShelfmark(id){
	var input = document.getElementById(id);
	var td = input.parentNode;
	var tr = td.parentNode;
	var tbody = tr.parentNode;
	tbody.removeChild(tr);
}

//end of functions for multiple entry fields
//
//================================================================================================
//Functions for Holdings and USA second databases

function updateFullRef(value){
		var url = '../edit/';
		var data = 'operation=references&q=' + value;		
		var cell = document.getElementById('refs_full');
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var text = transport.responseText;	
			cell.value = text;	
		}});			
}

function updateFullUsa(value){
		var url = '../edit/';
		var data = 'operation=usa&q=' + value;		
		var cell = document.getElementById('usa_full');
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var text = transport.responseText;	
			cell.value = text;	
		}});			
}

function showValue(value){
		var url = '../edit/';
		var data = 'operation=references&q=' + value;		
		var cell = document.getElementById('refdisplay');
		if (cell.childNodes[0]){
			cell.removeChild(cell.childNodes[0]);
		}
		var p = cell.appendChild(document.createElement('p'));
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var text = document.createTextNode(transport.responseText);	
			p.appendChild(text);	
		}});	
		cell.appendChild(p);
}

function showUsa(value){
		var url = '../edit/';
		var data = 'operation=usa&q=' + value;		
		var cell = document.getElementById('usadisplay');
		if (cell.childNodes[0]){
			cell.removeChild(cell.childNodes[0]);
		}
		var p = cell.appendChild(document.createElement('p'));
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var text = document.createTextNode('Full USA location: ' + transport.responseText);	
			p.appendChild(text);	
		}});	
		cell.appendChild(p);
		document.getElementById('usabutton').style.display = 'block';		
}


function clearRef(){
	var cell = document.getElementById('refdisplay');
	if (cell){
		for (var i=0; i < cell.childNodes.length; i++){
			cell.removeChild(cell.childNodes[i]);	
		}
		cell.appendChild(document.createElement('p'));
	}
}

function clearUsa(){
	var cell = document.getElementById('usadisplay');
	for (var i=0; i < cell.childNodes.length; i++){
		cell.removeChild(cell.childNodes[i]);	
	}
	cell.appendChild(document.createElement('p'));
	document.getElementById('usabutton').style.display = 'none';
}

function clearUsaText(){
	var cell = document.getElementById('usadisplay');
	if (cell){
		for (var i=0; i < cell.childNodes.length; i++){
			cell.removeChild(cell.childNodes[i]);	
		}
		cell.appendChild(document.createElement('p'));
	}
}



function editRef(){
	var abbrev = document.getElementById('510_a').value;
	abbrev = abbrev.replace(/&/g, '%26');
	if (abbrev.strip() == ' ' || abbrev.strip() == ''){
		alert('Please add abbreviated reference in the reference box first to ensure a duplicate reference is not created');
		return;
	}
	if (abbrev.strip() != ' ' && abbrev.strip() != ''){
		showValue(abbrev);
		var full = document.getElementById('refdisplay').childNodes[0].firstChild.nodeValue;
		full = full.replace(/&/g, '%26');	
	}
	else {
		full = ' ';
	}
	var span = document.createElement('span');
	span.appendChild(document.createTextNode('References Editing'));
	document.getElementById('subformtitle').removeChild(document.getElementById('subformtitle').firstChild);
	document.getElementById('subformtitle').appendChild(span);
	document.getElementById('subabbr').value = abbrev;
	document.getElementById('subfull').value = full;
	document.getElementById('formtype').value = 'refs';
	document.getElementById('popupform').style.display = 'block';
}


function editUsa(){
	var abbrev = document.getElementById('holdings_a').value;
	abbrev = abbrev.replace(/&/g, '%26');
	if (abbrev.strip() == ' ' || abbrev.strip() == ''){
		alert('Please add abbreviated library location in the library box first to ensure a duplicate entry is not created');
		return;
	}
	if (abbrev.strip() != ' ' && abbrev.strip() != ''){
		showUsa(abbrev);
		var full = document.getElementById('usadisplay').childNodes[0].firstChild.nodeValue;
		full = full.substring(full.indexOf(':')+2);
		full = full.replace(/&/g, '%26');	
	}
	else {
		full = ' ';
	}
	var span = document.createElement('span');
	span.appendChild(document.createTextNode('U.S.A. Locations Editing'));
	document.getElementById('subformtitle').removeChild(document.getElementById('subformtitle').firstChild);
	document.getElementById('subformtitle').appendChild(span);
	document.getElementById('subabbr').value = abbrev;
	document.getElementById('subfull').value = full;
	document.getElementById('formtype').value = 'usa';
	document.getElementById('popupform').style.display = 'block';
}

function checkUSA(){
	if (document.getElementById('holdings_country').value == '952'){
		document.getElementById('usabutton').style.display = 'block';
	}
	else {
		document.getElementById('usabutton').style.display = 'none';
		clearUsa()
	}
} 


//end of functions for Holdings and USA second databases

//================================================================================================
//autosuggest functions


//maps html element ids to indexes
var indexMap = new Array();
		indexMap['260_a'] = 'idx-publoc-exact';
		indexMap['260_b'] = 'idx-printer-exact';
		indexMap['author'] = 'idx-author-exact';
		indexMap['510_a'] = 'idx-key-refs-exact';
		indexMap['refs_a'] = 'idx-key-refs-exact';
		indexMap['holdings_a'] = 'idx-key-usa';
		indexMap['usa_a'] = 'idx-key-usa';
		indexMap['ISTCNo'] = 'idx-ISTCnumber';


//the option currently selected - used to select but keep focus on textbox
var optionSel = -1;

var ajaxSuggest = null;



function suggestDelay(id, e){
	clearTimeout(timeout);
	timeout = setTimeout(function() {suggest(id, e)}, 1000);
}


function suggest(id, e){
	var suggestBox = document.getElementById('suggestBox');
	var tid = id;
	if (tid == 'holdings_a'){
		if (document.getElementById('holdings_country').value != '952'){
			return;
		}		
	}
	//16 - shift 20 - capslock
	if (keyCheck(e) == 16 || keyCheck(e) == 20){
		return;
	}
	//up
	if (keyCheck(e) == 38){
		optionSel = optionSel - 1;
		if (optionSel < 0){
			optionSel = 0;
		}
		suggestBox.options[optionSel].selected = true;		
	}
	//down
	else if (keyCheck(e) == 40){
		optionSel = optionSel + 1;
		if (optionSel > suggestBox.options.length-1){
			optionSel = suggestBox.options.length-1;
		}
		suggestBox.options[optionSel].selected = true;
	}
	//return
	else if (keyCheck(e) == 13){
		selectClick(suggestBox, tid, 'key');
	}
	else {	
		var element = document.getElementById(id);
		var index = indexMap[id];
	
		//delete any existing boxes		
		if (suggestBox){
			suggestBox.parentNode.removeChild(suggestBox);
		}
		if (tid == 'refs_a'){
			updateFullRef('');
		}
		if (tid == 'usa_a'){
			updateFullUsa('');
		}
		if (element.value != ''){
		//AJAX call to get values from index
			var terms = '';
			var url = 'suggest.html';
			var data = 'operation=suggest&i=' + index + '&s=' + element.value;
			var ajaxSuggest = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var response = transport.responseText;
				terms = response.substring(8,response.indexOf('</select>'));				
			}});	
			createSuggestBox(terms, tid, element);
		}	
	}
}


function createSuggestBox(terms, tid, element){
	if (terms != ''){
		var termList = terms.split(' | ');
	}
	else {
		var termList = [];
	}
	var len = parseInt(termList.length);
	if (len > 10){
		//only display 10 at a time
		len = 10;
	}
	if (len > 0){ 
		//create the select box
		var select = document.createElement('select');
		select.setAttribute('id', 'suggestBox');
		select.setAttribute('size', len);
		select.className = 'suggest';
		select.style.position = 'absolute';
		select.style.width = element.offsetWidth + 'px';
		var string = tid;
		select.onclick = function () {selectClick(this, string, 'mouse'); };
		if (tid == '510_a' || 'ISTCNo'){
			for(var i=0; i < termList.length; i++) {
				var value = termList[i].substring(0, termList[i].lastIndexOf(' ('));
		   		select.options[i] = new Option(value, value);
			}
		}
		else {
			for(var i=0; i < termList.length; i++) {
		   		select.options[i] = new Option(termList[i], termList[i].substring(0, termList[i].lastIndexOf(' (')));
			}					
		}
		element.parentNode.appendChild(select);
		if (tid == 'refs_a' || tid == '510_a'){
			clearRef();
		}
		if (tid == 'usa_a'|| tid == 'holdings_a'){
			clearUsaText();
		}
		optionSel = -1;		    	
	}
}


function selectClick(elem, target, mode){
	var element = elem;
	var targetElem = document.getElementById(target);
	if (optionSel != -1 || mode == 'mouse'){
		targetElem.value = element.value;
	}
	targetElem.parentNode.removeChild(element);
	if (targetElem.id == '510_a'){
		clearRef();
		showValue(targetElem.value);
	}
	if (targetElem.id == 'refs_a'){
		updateFullRef(targetElem.value);
	}
	if (targetElem.id == 'usa_a'){
		updateFullUsa(targetElem.value);
	}
	if (targetElem.id == 'holdings_a'){
		showUsa(targetElem.value)
	}
}


//checks which key was pressed - list available here http://webonweboff.com/tips/js/event_key_codes.aspx
function keyCheck(e){
   	var keyId = (window.event) ? event.keyCode : e.keyCode;
	return keyId;	   
}


function clearSuggests(){
	if (document.getElementById('suggestBox')){
		var suggest = document.getElementById('suggestBox');
		suggest.parentNode.removeChild(suggest);	
	}
}

function getAll(letters, type){
	var url = '../edit/';
	var data = 'operation=all&letters=' + letters + '&type=' + type;
	document.getElementById('colcontainer').innerHTML = '';
	if (letters != ''){
		var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
			var response = transport.responseText;
			document.getElementById('colcontainer').innerHTML = response;
	
		}});	
	}
}

var op = null;

function confirmOp(){
	switch(op) {
		case 'unindex':
			var msg = 'This operation will PERMANENTLY remove the file from the hard-disk. The record will also be removed from all indexes, which may take some time. Are you sure you wish to continue?';
			break
		case 'delete':
			var msg = 'This operation will PERMANENTLY remove the file from the hard-disk. Are you sure you wish to continue?';
			break
			
		default:
			if (arguments.length == 1){
				/*hopefully a message we should send*/
				var msg = arguments[0];
			}
			break
	}
	if (msg) {
		if (window.confirm) { return window.confirm(msg); }
		else if (confirm) { return confirm(msg); }
		else { return true; } // no mechanism for confirmation supported by browser - go ahead anyway
	} else {return true; } // no requirement for confirmation
}


// end of auto suggest functions
// 
//
//================================================================================================
//keyboard related functions

var currentCharTable = 'lower';

function toggleKeyboard(){
  	var keyboard = ($('keyboard')); 
  	keyboard.toggle();  
  	showCharTable('lower');
}


function showCharTable(type){
	if (type == 'lower'){
  		($('chartablelower')).style.display = 'block';
  		($('chartableupper')).style.display = 'none';
  	}
  	else if (type == 'upper'){
  		($('chartableupper')).style.display = 'block';
  		($('chartablelower')).style.display = 'none';   	
  	}
  	else {
		($('chartable' + currentCharTable)).style.display = 'block';
  	}
}


function hideCharTable(){
	if (($('chartableupper')).style.display == 'block'){
		currentCharTable = 'upper';
	}
	else {
		currentCharTable = 'lower';
	}
  	($('chartableupper')).style.display = 'none';
  	($('chartablelower')).style.display = 'none';  	
}


//====================================================================================================
//
// Submit Functions

function submitSubForm(){
	
	var operation = document.getElementById('formtype').value;

	var abbrev = document.getElementById('subabbr').value;
	var full = document.getElementById('subfull').value;
	if (abbrev.strip() == '' || full.strip() == ''){
		alert('All fields must me completed before submitting');
		return;
	}
	var url = '../edit/';
	if (operation == 'usa'){
		var data = 'operation=submitusasub';
	}
	else {
		var data = 'operation=submitrefsub';
	}
	data += '&abbrev=' + abbrev + '&full=' + full;
	var outcome = 'failed';
	var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
		var response = transport.responseText;
		outcome = response; 
	}});	
	if (outcome == 'locked'){
		alert('Another user is already indexing this database so no files can currently be indexed. Please try again in 10 minutes.');
	}
	else if (outcome == 'success'){
		alert('The data has been saved successfully');
		hidePopup();
	}
	else {
		alert('The data was not saved successfully, please try again.');
	}
}

function validate_ISTCNo(string){
	var istcNo = string;
	var match = istcNo.match(/^\w{2}\d{8}$/);
	if (match == null){
		return false;
	}
	else {
		return true;
	}
}

function saveForm(){
	if (document.getElementById('ISTCNo').className != 'readonly'){
		var istcNo = document.getElementById('ISTCNo').value
		if (istcNo.strip() != '' && validate_ISTCNo(istcNo.strip())){
			//already in main db
			var url = '../edit/';
			var data = 'operation=checkDir&id=' + istcNo;
			var error = false;
			var conflict = '';
			var owner = '';
			var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var response = transport.responseText;
				conflict = response;
				
			}});		
			if (conflict == 'true'){
				alert('A file with this ISTC number already exists in the database. You will need to edit that file rather than create a new one.');
				return false;
			}
			//already being created
	
			data = 'operation=checkStore&id=' + istcNo.strip();
			error = false;
			var conflict = '';
			var owner = '';
			var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var response = transport.responseText;
				if (response.substring(0, 4) == "<!--"){
					error = true;
				}			
				conflict = response.substring(response.indexOf('<value>')+7, response.indexOf('</value>'));
				if (response.indexOf('<owner>') > -1){
					owner = response.substring(response.indexOf('<owner>')+7, response.indexOf('</owner>'));
				}
			}});	
			if (conflict == 'true'){
				if (owner == 'user'){
					alert('You already have a draft file with this ISTC number in the draft file store. The draft must be deleted before you can create a new draft with this ISTC number');
					return false;
				}
				else {
					alert(owner + ' already has a draft file with this ISTC number in the draft file store. You will not be able to create a file with this ISTC Number unless the other user deletes their version.')
					return false;					
				}
			}					
			save();
		}
		else {
			alert('The ISTC number must be completed correctly before saving this record. It should contain two letters followed by eight numbers');
			return false;
		}
	}
	else {
		save();
	}
}

function save(){
	var istcNo = document.getElementById('ISTCNo').value.strip();			
	var reload = false;
	var form = document.getElementById('mainform');	
	var timestamp;
	document.getElementById('opvalue').value = 'save';
	var url = '../edit/';
	var data = ($('mainform')).serialize();
	var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
		var response = transport.responseText;
		timestamp = response;
	}});
	var span = document.getElementById('savetime');
	var time = document.createTextNode(timestamp);
	if (span.firstChild.nodeValue.strip() == ''){
		reload = true;
	}
	span.removeChild(span.firstChild);
	span.appendChild(time);
	if (reload == true){
		window.location.href='../edit/?operation=load&recid=' + istcNo;
	}
	return true;
}

function submitForm(op){
	if(save()){	
		document.getElementById('opvalue').value = op;
		if (op == 'discard'){
			var ok = confirmOp('You are about to delete this draft file. All changes made since it was last submitted to the database will be lost. The live data will not be affected. \nAre you sure you want to continue?')
			if (ok){
				document.getElementById('mainform').submit();
			}
			else {
				return;
			}
		}
		else if (op == 'file'){
			var ok = confirmOp('This operation will write this record to the data directory and it will be available for searching the next time the database is rebuilt. \nAre you sure you want to continue?')
			if (ok){
				document.getElementById('mainform').submit();
			}
			else {
				return;
			}
		}
		else if (op == 'index'){
			var ok = confirmOp('This operation will index this record and make it immediately available for searching. This operation may take some time. \nAre you sure you want to continue?')
			if (ok){
				document.getElementById('mainform').submit();
			}
			else {
				return;
			}
		}
		else {
			document.getElementById('mainform').submit();
		}
	}
}


function checkButtons(){
	if (document.getElementById('ISTCNo').value.strip() == ''){
		document.getElementById('xmlbutton').setAttribute('disabled', 'true');
		document.getElementById('marcbutton').setAttribute('disabled', 'true');
		document.getElementById('emailbutton').setAttribute('disabled', 'true');		
		document.getElementById('filebutton').setAttribute('disabled', 'true');
		document.getElementById('indexbutton').setAttribute('disabled', 'true');		
		
	}
}


function deleteFromStore(){
	var recid = null;

	if (document.getElementById('storeDirForm').recid.length){
		for (var i=0; i < document.getElementById('storeDirForm').recid.length; i++) {
			if (document.getElementById('storeDirForm').recid[i].checked) {
		      	recid = document.getElementById('storeDirForm').recid[i].value;
		    }
		}
	}
	else {
		if (document.getElementById('storeDirForm').recid.checked) {
			recid = document.getElementById('storeDirForm').recid.value;
		}
	}
	if (recid == null) {
		return;
	}
	else {
		var ok = confirmOp('You are about to delete ' + recid.substring(0, recid.lastIndexOf('-')) + ' from the draft file store. All changes made since it was last submitted to the database will be lost. The live data will not be affected. \nAre you sure you want to continue?')
		if (ok){
			deleteRec(recid)
		}
		else {
			return;
		}
	}
}

function deleteRec(id){
	var url = '../edit/';
	var data = 'operation=discard&recid=' + encodeURIComponent(id);
	var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
		location.href="../edit/edit.html";		    
	}});		
}

//==================================================================================================
//
//Popup Div Functions

function hidePopup(){
	document.getElementById('popupform').style.display = 'none';
}

function showPopup(){
	document.getElementById('popupform').style.display = 'block';
}

