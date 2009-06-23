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
// Copyright: &copy; University of Liverpool 2009
//
// Version History:
// 0.01 - 29/05/2008 - CS - Basic functions for record display
*/ 


var timeout;
var op = null;





function addLoadEvent(func) {
	var oldonload = window.onload;
	if (typeof window.onload != 'function') {
    	window.onload = func;
	} else {
	window.onload = function() {
			if (oldonload) {
				oldonload();
			}
			func();
		}
	}
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
	if (document.getElementById('expandedbib')){
		if (document.getElementById('expandedbib').checked == true){
			document.getElementById('expand').value = "true";
		}
		else if (document.getElementById('expandedbib')){
			document.getElementById('expand').value = "false";
		}
	}	
	var form = document.getElementById('mainform');
	var table = form.getElementsByTagName('table')[0];
	if (table){
		var checkboxes = table.getElementsByTagName('input');
		var valid = false;
		for (var i=0; i<checkboxes.length; i++){
			if (checkboxes[i].checked){
				valid = true;
				break;
			}
		}
		if (valid){	
			document.getElementById('opvalue').value = op;
			document.getElementById('mainform').submit();
		}
		else {
			alert('Please select records first');
		}
	}
	else {
		document.getElementById('opvalue').value = op;
		document.getElementById('mainform').submit();	
	}
}



function changePage(){

	var select = document.getElementById('pagejump');
	var value = select.value;
	if (value != 'null') {
		location.href = value;
	}
}

