/*
// Script:	searchForm.js
// Version:	0.05
// Description:
//          JavaScript functions used in the Cheshire3 EAD search/retrieve and display interface 
//          - part of Cheshire for Archives v3.x
//
// Language:  JavaScript
// Author:    John Harrison <john.harrison@liv.ac.uk>
// Date:      25 January 2007
//
// Copyright: &copy; University of Liverpool 2005, 2006, 2007
//
// Version History:
// 0.01 - 03/08/2006 - JH - Search form DOM manipulation functions pasted in from previous script for easier error tracking etc.
// 0.02 - 24/10/2006 - JH - Additions for adding/removing phrase option to relation drop-down when necessary
// 0.03 - 11/12/2006 - JH - Mods for compatibility with IE7
//							- get elements by id rather than name wherever possible
//							- use innerHTML to setup radio buttons
// 0.04 - 14/12/2006 - JH - Search form state maintained in cookie. Reset function added.
// 0.05 - 25/01/2007 - JH - Muchos new stuff in anticipation of date searching
//
*/



var kwRelationList = new Array('all|||All', 'any|||Any');
var exactRelationList = new Array('exact|||Exactly');
var proxRelationList = new Array('=|||Phrase', 'exact|||Exactly');
var dateRelationList = new Array('%3C|||Before', '%3E|||After', 'exact|||Exactly');
var indexList = new Array('cql.anywhere|||General Keywords', 'dc.creator|||Author', 'dc.title|||Title', 'bib.originPlace|||Location of Print', 'dc.publisher|||Printer', 'dc.identifier|||ISTC Number', 'dc.format|||Format', 'norzig.posessingInstitution|||Location', 'c3.idx-year|||Start or exact Year (008)','dc.date|||Publication Date', 'dc.language|||Language', 'istc.BLshelfmark|||BL Shelfmark');



function updateSelects(current){
	var idxSelect = document.getElementById('fieldidx' + current);
	var relSelect = document.getElementById('fieldrel' + current);
	if  (!idxSelect || !relSelect || !idxSelect.options || !relSelect.options) {
		return
	}
	relSelect.options[relSelect.selectedIndex].selected = false;
	var iSelIdx = idxSelect.selectedIndex;

	var rSelIdx = 0;
	
	// complex conditional to decide available relations
	var relationList = new Array()
	if (iSelIdx != 5 && iSelIdx != 6 && iSelIdx != 10 && iSelIdx != 11) { var relationList = kwRelationList; }
	if (iSelIdx == 5 || iSelIdx == 6 || iSelIdx == 10 || iSelIdx == 11) { var relationList = exactRelationList; }
	if (iSelIdx == 8) {var relationList = dateRelationList; var rSelIdx = 2;}
	if (iSelIdx > 0 && relationList == kwRelationList) { var relationList = relationList.concat(proxRelationList); }	
	
	// now replace existing relation select element
	relSelect.parentNode.insertBefore(createSelect('fieldrel' + current, relationList, rSelIdx), relSelect);
	relSelect.parentNode.removeChild(relSelect);

}

function addSearchClause(current, boolIdx, clauseState){
  if ( !document.getElementById || !document.createElement ) {
 	return;
  }
  //var form = document.getElementsByName('searchform')[0]
  var insertHere = document.getElementById('addClauseP');
  if (current > 0) {
	  newBool = createBoolean(current, boolIdx);
	  insertHere.parentNode.insertBefore(newBool, insertHere);
	  //form.insertBefore(boolOp, form.childNodes[insertBeforePosn])
  }
  current++;
  newClause = createClause(current, clauseState);
  insertHere.parentNode.insertBefore(newClause, insertHere);
  //form.insertBefore(clause, form.childNodes[insertBeforePosn+1])
  document.getElementById('addClauseLink').href = 'javascript:addSearchClause(' + current + ');';
}

function createBoolean(current, selIdx){
	/* radio buttons cannot be created by DOM for IE - use innerHTML instead */
	if (!selIdx) {var selIdx = 0;}
	var pElem = document.createElement('p');
	pElem.setAttribute('id', 'boolOp' + current);
	pElem.setAttribute('class', 'boolOp');
	var boolList = new Array('and/relevant/proxinfo', 'or/relevant/proxinfo', 'not');
	var inputs = new Array();
	for (var i=0;i<boolList.length;i++) {
		var val = new String(boolList[i]);
		if (val.indexOf('/') > 0) {
			var shortName = val.substring(0, val.indexOf('/'));
		} else {
			var shortName = val;
		}
		inputs[i] = '<input type="radio" name="fieldbool' + current + '" value="' + val + '" id="fieldbool' + current + '-' + shortName + '"';
		if (i == selIdx) {
			inputs[i] += ' checked="checked"'
		}
		inputs[i] += '/><label for="fieldbool' + current + '-' + shortName + '">' + shortName.toUpperCase() + '&nbsp;&nbsp;</label>';
	}
  	pElem.innerHTML = inputs.join('\n');
	return pElem
}

function createClause(current, clauseState){
	if (!clauseState) {var clauseState = '0,';}
	var parts = clauseState.split(',');
	var pElem = document.createElement('p')
	pElem.setAttribute('id', 'searchClause' + current);
	pElem.setAttribute('class', 'searchClause')

	// relation select
	var rSelIdx = parts.shift();
	// complex conditional to decide available relations
	var relationList = new Array()
	if (iSelIdx != 5 && iSelIdx != 6 && iSelIdx != 10 && iSelIdx != 11) { var relationList = kwRelationList; }
	if (iSelIdx == 5 || iSelIdx == 6 || iSelIdx == 10 || iSelIdx == 11) { var relationList = exactRelationList; }
	if (iSelIdx == 8) {var relationList = dateRelationList; var rSelIdx = 2;}
	if (iSelIdx > 0 && relationList == kwRelationList) { var relationList = relationList.concat(proxRelationList); }
	
	// text input
	var inputElem = document.createElement('input');
	inputElem.type = 'text';
	inputElem.size = 30;
	inputElem.name = 'fieldcont' + current;
	inputElem.id = 'fieldcont' + current;
	
	// index select
	var iSelIdx = parts.shift();
	var idxSelect = createSelect('fieldidx' + current, indexList, iSelIdx)
	idxSelect.onchange = new Function('updateSelects(' + current + ');')
	pElem.appendChild(document.createTextNode(' '))
	pElem.appendChild(idxSelect)
        pElem.appendChild(document.createTextNode(' '  ))
        
	pElem.appendChild(document.createTextNode(' for: '))

	// last entered value
	inputElem.value = parts.join(',');
	pElem.appendChild(inputElem);
	pElem.appendChild(createSelect('fieldrel' + current, relationList, rSelIdx));		
	return pElem;
}

function createSelect(name, optionList, selIdx){
	// set 1st option as selected by default
	if (!selIdx) {var selIdx = 0;}
	var selectElem = document.createElement('select')
	selectElem.id = name;
  	selectElem.name = name;
	for (var i=0; i < optionList.length; i++){
		var optionData = optionList[i].split('|||')
		var optionElem = document.createElement('option')
		optionElem.value = optionData[0];
		optionElem.innerHTML = optionData[1];
		
		if (i == selIdx) {optionElem.selected = 'selected'}
		selectElem.appendChild(optionElem)
	}
	return selectElem
}

function removeClause(current) {
	var pElem = document.getElementById('boolOp' + (current-1));
	if (pElem) {
		pElem.parentNode.removeChild(pElem);
	}
	var pElem = document.getElementById('searchClause' + current);
	pElem.parentNode.removeChild(pElem);
	document.getElementById('addClauseLink').href = 'javascript:addSearchClause(' + current + ');';
}

function resetForm() {
	var i = 1;
	while (document.getElementById('searchClause' + i)) {
		removeClause(i);
		i++;
	}
	addSearchClause(0);
	document.getElementById('addClauseLink').href = 'javascript:addSearchClause(1);';
	setCookie('eadsearchform', '');
}

function formToString() {
	var i = 0;
	var fields = new Array();
	var bools = new Array();
	while (document.getElementById('fieldcont' + (i+1)) && document.getElementById('fieldcont' + (i+1)).value != "") {
		bools[i] = 0;
		if (i > 0) {
			var boolgrp = document.getElementsByName('fieldbool' + i);
			//while (!boolgrp[0].value) {boolgrp = boolgrp.slice(1);}
			for (var j=0;j<boolgrp.length;j++) {
				if (boolgrp[j].checked == true) {
					bools[i] = j;
				}
			}
		}
		i++;
		var idx = document.getElementById('fieldidx' + i).selectedIndex;
		var rel = document.getElementById('fieldrel' + i).selectedIndex;
		var cont = document.getElementById('fieldcont' + i).value;
		fields[i-1] = new Array(idx, rel, cont).join();
	} 
	stateString = fields.join('||') + '<CLAUSES|BOOLS>' + bools.join('||');
	return stateString;
}

function formFromString(s) {
	if (s && s.length > 0) {
		var parts = s.split('<CLAUSES|BOOLS>');
	} else {
		var parts = new Array()
	}
	
	if (parts.length == 2) {
		var clauseList = parts[0].split('||');
		var boolList = parts[1].split('||');
		for (var i=0;i<clauseList.length;i++) {
			addSearchClause(i, boolList[i], clauseList[i]);
		}
	} else {
		// no state - initialise empty search form
		addSearchClause(0);
	}

	return;
}
