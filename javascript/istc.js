/*
// Program:   istc.js
// Version:   0.0x
// Description:
//            JavaScript functions used in the Cheshire3 ISTC search/retrieve and display interface 
//            
//
// Language:  JavaScript
// Author:    Catherine Smith <catherine.smith@liv.ac.uk>
// Date:      29/05/2008
//
// Copyright: &copy; University of Liverpool 2008
//
// Version History:
// 0.01 - 29/05/2008 - CS - Basic functions for record display and edit interfaces
*/ 



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

//================================================================================================
// display record functions

function expandRefs(){
	var short = document.getElementById('abbrRefs');
	var long = document.getElementById('fullRefs');
	long.style.display = 'block';
	short.style.display = 'none';
	
}

function collapseRefs(){
	var short = document.getElementById('abbrRefs');
	var long = document.getElementById('fullRefs');
	long.style.display = 'none';
	short.style.display = 'block';
}

function submitForm(op){
	if (op == 'print'){
		if (document.getElementById('expandedbib')){
			if (document.getElementById('expandedbib').checked == true){
				document.getElementById('expand').value = "true";
			}
		}
		document.getElementById('mainform').submit();
	}
	else {
		if (document.getElementById('expandedbib')){
			if (document.getElementById('expandedbib').checked == true){
				document.getElementById('expand').value = "true";
			}
		}
		document.getElementById('opvalue').value = op;
		document.getElementById('mainform').submit();
	}
}




//================================================================================================
//Functions for multiple entry fields

var nameCount = 0;

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
    	textbox = rows[i].getElementsByTagName('input')[0]
    	if (textbox.value != ""){
    		valueString += textbox.id + ' | ' + textbox.value + ' ||| ';
    		textString += textbox.value + ' ';  		
    	}   
    	else {
    		valueString += textbox.id + ' |   ||| ';
    	}
    	textbox.value = '';
    }
           
    /* add to DOM */
    var div = document.getElementById('added' + s.toLowerCase());
    var list = document.getElementById('added' + s.toLowerCase() + 'list');
    var item = document.createElement('li');
    item.setAttribute('id', 'li' + s + nameCount);
    var txtnode = document.createTextNode(textString); 
	var number = nameCount;
    nameDiv = document.createElement('div');
    nameDiv.setAttribute('class', 'multipleEntry');
    nameDiv.onclick = function () {editEntry(s, number); },   
    nameDiv.setAttribute('title', 'Click to edit');
    nameDiv.appendChild(txtnode);
    
    var icondiv = createIcons(s);

    var wrapper = document.createElement('div');
    wrapper.setAttribute('id', s + nameCount);  
    wrapper.appendChild(icondiv);
    wrapper.appendChild(nameDiv);   
    item.appendChild(wrapper);
    
    var br = document.createElement('br');
    br.setAttribute('id', s + nameCount + 'br');
    item.appendChild(br);
    
    var hidden = document.createElement('input');
    hidden.setAttribute('type', 'hidden');
    hidden.setAttribute('name', s);
    hidden.setAttribute('id', s + nameCount + 'xml'); 
    hidden.setAttribute('value', valueString);

    item.appendChild(hidden);
    
    list.appendChild(item);
    if (div.style.display = 'none'){
    	div.style.display = 'block';
    }
    if (list.getElementsByTagName('li').length > 1){
		Sortable.create('added' + s.toLowerCase() + 'list', {handle:'handle', constraint: 'vertical' });
	}
	else {
		Sortable.destroy('added' + s.toLowerCase() + 'list');
	}
    nameCount++;   	 
}




function createIcons(s){
   var icondiv = document.createElement('div');
   icondiv.className = 'icons'; 

   var d = "'" + s + nameCount + "'";
   var s = "'" + s + "'";
   /* the delete icon */
   innerHTMLString = '<a onclick ="deleteEntry(' + d + ');" title="delete entry"><img src = "/istc/images/deletesmall.gif" id="delete' + nameCount + '"/></a>'; 
	
	/*the reorder icon */
   innerHTMLString += '<span class="handle">move</span>'; 
   
   icondiv.innerHTML = innerHTMLString;
   return icondiv
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
  
  	var string = document.getElementById(s + number + 'xml').value;
  	var values = string.split(' ||| ');
  
 	var tableDiv = ($(type + 'table'));

  	var table = tableDiv.getElementsByTagName('tbody')[0];
  	var rows = table.getElementsByTagName('tr');
  	var inputs = table.getElementsByTagName('input');
  	
  	// replace values in order
  	for (var i = 0; i< values.length-1; i++){  
  		value = values[i].split(' | ');
  		inputs[i].value = value[1];
  	}
  	//delete the access point you are now editing
  	deleteEntry(s + number);	
}

//end of functions for multiple entry fields

//================================================================================================
//autosuggest functions


//maps html element ids to indexes
var indexMap = new Array();
		indexMap['imprints_a'] = 'idx-location';
		indexMap['imprints_b'] = 'idx-printer';
		indexMap['author'] = 'idx-author';

//the option currently selected - used to select but keep focus on textbox
var optionSel = 0;



function suggest(id, e){

	var suggestBox = ($('suggestBox'));
	var tid = id;
	
	if (keyCheck(e) == 38){
		optionSel = optionSel - 1;
		if (optionSel < 0){
			optionSel = 0;
		}
		suggestBox.options[optionSel].selected = true;		
	}
	else if (keyCheck(e) == 40){
		optionSel = optionSel + 1;
		if (optionSel > suggestBox.options.length-1){
			optionSel = suggestBox.options.length-1;
		}
		suggestBox.options[optionSel].selected = true;
	}
	else if (keyCheck(e) == 13){
		selectClick(suggestBox, tid);
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
			var data = 'operation=suggest&i=' + index + '&s=' + element.value.toLowerCase();
			var ajax = new Ajax.Request(url, {method:'post', asynchronous:false, postBody:data, evalScripts:true, onSuccess: function(transport) {	
				var response = transport.responseText;
				terms = response.substring(8,response.indexOf('</select>'));
				termList = terms.split(' | ');
				len = parseInt(terms.split(' | ').length);
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
					select.onclick = function () {selectClick(this, tid); };
					select.onkeyup = function (e) {selectReturn(this, tid, e); };
					for(var i=0; i < termList.length; i++) {
					   select.options[i] = new Option(termList[i], termList[i].substring(0, termList[i].lastIndexOf(' (')));
					}
					element.parentNode.appendChild(select);
					select.options[0].selected = true;
					optionSel = 0;
				}
						    
			}});		
		}	
	}
}


function selectClick(elem, target){
	var element = elem;
	var targetElem = ($(target)); 
	targetElem.value = element.value;
	targetElem.parentNode.removeChild(element);
}


function selectReturn(elem, target, e){
	if (keyCheck(e) == 13){
		var element = elem;
		var targetElem = ($(target)); 
		targetElem.value = element.value;
		targetElem.parentNode.removeChild(element);
	}
}

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



