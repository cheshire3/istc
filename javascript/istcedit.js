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


//================================================================================================
//Functions for multiple entry fields

var nameCount = 0;

var indicators = new Array();
		indicators['100'] = '1-0';
		indicators['245'] = '1-0';
		indicators['510'] = '4-0';
		indicators['959'] = '1-0';

function addEntry(s){

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
    	if (textbox.value != ""){
    		valueString += textbox.id + ' | ' + textbox.value + ' ||| ';
    		textString += textbox.value + ' ';  		
    	}   
    	else {
    		valueString += textbox.id + ' |   ||| ';
    	}
    	textbox.value = '';
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
    p.className = 'float'; 

    p.onclick = function () {editEntry(s, number); };
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
    p.appendChild(txtnode);
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
  	else if (list.getElementsByTagName('li').length == 1){
  		Sortable.destroy(list.getAttribute('id'));
  	}
}


/* repopulate the access point with the details from the given entry so they can be edited, s is either the name of the access point or the name of the access point
followed by '_formgen' which is used to maintain distinct ids between access points read in from existing xml and those created in the current form,
number is the number which forms part of the unique id */
function editEntry(s, number){
	
	var type = s.substring(0, s.indexOf('_formgen'));
  	if (type == '') {
  		type = s;
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


function registerLists(){
	added = document.getElementsByClassName('added');
	for (var i = 0; i< added.length; i++){
		if (added[i].style.display == 'block'){
			list = document.getElementById(added[i].id + 'list');
			if (list.getElementsByTagName('li').length > 1){
				Sortable.create(added[i].id + 'list', {handle:'handle', constraint: 'vertical' });
			}
		}
	}
}


function showValue(value){
		var url = '/istc/edit/';
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

/*
function getFullRef(element){
	clearRef();
	var cell = document.getElementById('refdisplay');
	var p = cell.appendChild(document.createElement('p'));
	var value = element.value;
	var url = '/istc/edit/';
	var data = 'operation=references&q=' + value;
	var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
		var text = document.createTextNode(transport.responseText);	
		p.appendChild(text);
		cell.appendChild(p);	
	}});		
}*/


/*
function getFormRef(e){
	
	var element;
	if (!e) {
		var e = window.event;
	}
	if (e.target){
		element = e.target;
	}else{
		element = window.event.srcElement;
	}
	if (element.id == 'addedreferences') {
		clearRef();
		var cell = document.getElementById('refdisplay');
		var p = cell.appendChild(document.createElement('p'));
		value = document.getElementById('510_a').value;
		if (value != "" && value != " "){
			var url = '/istc/edit/';
			var data = 'operation=references&q=' + value + '&r=False';
			var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var text = document.createTextNode(transport.responseText);
				p.appendChild(text);
			}});
		}
		cell.appendChild(p);		
	}
}*/



function clearRef(){
	var cell = document.getElementById('refdisplay');
	for (var i=0; i < cell.childNodes.length; i++){
		cell.removeChild(cell.childNodes[i]);	
	}
	cell.appendChild(document.createElement('p'));
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
	document.getElementById('subAbbrRef').value = abbrev;
	document.getElementById('subFullRef').value = full;
	document.getElementById('refPopup').style.display = 'block';
	
	

}
//end of functions for multiple entry fields

//================================================================================================
//autosuggest functions


//maps html element ids to indexes
var indexMap = new Array();
		indexMap['260_a'] = 'idx-kwd-publoc';
		indexMap['260_b'] = 'idx-printer';
		indexMap['author'] = 'idx-author';
		indexMap['510_a'] = 'idx-key-refs-exact';


//the option currently selected - used to select but keep focus on textbox
var optionSel = -1;

var ajaxSuggest = null;



function suggestDelay(id, e){
	clearTimeout(timeout);
	timeout = setTimeout(function() {suggest(id, e)}, 1000);
}


function suggest(id, e){

	var suggestBox = ($('suggestBox'));
	var tid = id;
	
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
		var element =($(id));
		var index = indexMap[id];
	
		//delete any existing boxes		
		if (suggestBox){
			suggestBox.parentNode.removeChild(suggestBox);
		}
		if (element.value != ''){
		//AJAX call to get values from index
			var url = '/istc/edit/';
			var data = 'operation=suggest&i=' + index + '&s=' + element.value;
			var ajaxSuggest = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var response = transport.responseText;
				var terms = response.substring(8,response.indexOf('</select>'));
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
					select.onclick = function () {selectClick(this, tid, 'mouse'); };
					select.onkeyup = function (e) {selectReturn(this, tid, e); };
					if (tid = '510_a'){
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
					optionSel = -1;
				}
						    
			}});		
		}	
	}
}


function selectClick(elem, target, mode){
	var element = elem;
	var targetElem = ($(target));
	if (optionSel != -1 || mode == 'mouse'){
		targetElem.value = element.value;
	}
	targetElem.parentNode.removeChild(element);
	if (targetElem.id == '510_a'){
		clearRef();
		showValue(targetElem.value);
	}
}

/*
function selectReturn(elem, target, e){
	if (keyCheck(e) == 13){
		var element = elem;
		var targetElem = ($(target)); 
		targetElem.value = element.value;
		targetElem.parentNode.removeChild(element);
		if (target == '510_a'){
			showValue(element.value);
		}
	}
}*/

//checks which key was pressed - list available here http://webonweboff.com/tips/js/event_key_codes.aspx
function keyCheck(e){
   	var keyId = (window.event) ? event.keyCode : e.keyCode;
	return keyId;	   
}





// end of auto suggest functions
// 
//
//================================================================================================
//keyboard related functions

function toggleKeyboard(){
  	var keyboard = ($('keyboard')); 
    keyboard.style.top = '100px';
    keyboard.style.left = '10px';
  	keyboard.toggle();  
  	showCharTable();
}


function showCharTable(){
  	($('chartable')).style.display = 'block';
}


function hideCharTable(){
  	($('chartable')).style.display = 'none';
}


//==================================================================================================
//
// Submit Functions

function submitReference(){
	var abbrev = document.getElementById('subAbbrRef').value;
	var full = document.getElementById('subFullRef').value;
	if (abbrev.strip() == '' || full.strip() == ''){
		alert('All fields must me completed before submitting');
		return;
	}
	var url = '/istc/edit/';
	var data = 'operation=submitref&abbrev=' + abbrev + '&full=' + full;
	var outcome = 'unsuccessful';
	var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
		var response = transport.responseText;
		if (response == 'success'){
			output = 'success';
		}
	}});	
	if (output = 'success'){
		alert('The reference has been saved successfully');
		showValue(abbrev)
		hideRefPopup();
	}
	else {
		alert('The reference was not saved successfully, please try again.');
	}
}

function submitForm(op){
	if (document.getElementById('expandedbib')){
		if (document.getElementById('expandedbib').checked == true){
			document.getElementById('expand').value = "true";
		}
		else if (document.getElementById('expandedbib')){
			document.getElementById('expand').value = "false";
		}
	}	
	form = document.getElementById('mainform');


	document.getElementById('opvalue').value = op;
	document.getElementById('mainform').submit();	
	
}

//==================================================================================================
//
//Popup Div Functions

function hideRefPopup(){
	document.getElementById('refPopup').style.display = 'none';
}

function showRefPopup(){
	document.getElementById('refPopup').style.display = 'block';
}