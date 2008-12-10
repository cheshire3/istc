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



var kwRelationList = new Array('all|||all of these words', 'any|||any of these words');
var exactRelationList = new Array('exact|||exactly');
var phraseRelationList = new Array('=|||as a phrase');
var proxRelationList = new Array('=|||as a phrase', 'exact|||exactly');
var dateRelationList = new Array('%3C|||before this year', '%3E|||after this year', 'exact|||exactly');
var indexList = new Array('cql.anywhere|||General Keywords', 'dc.creator|||Author', 'dc.title|||Title', 'bib.originPlace|||Place of Printing', 'istc.countryOfPrint|||Country of Printing',  'dc.publisher|||Printer', 'istc.referencedBy|||Bibliographical References', 'dc.identifier|||ISTC Number', 'dc.format|||Format', 'norzig.posessingInstitution|||Location of Copy', 'istc.countryOfCopy|||Country of Copy', 'c3.idx-year|||Start or exact Year (008)','dc.date|||Publication Date', 'dc.language|||Language', 'istc.BLshelfmark|||BL Shelfmark');

var formatList = new Array ('4to|||4to', '8vo|||8vo', '16mo|||16mo', 'fo|||fo', 'broadside|||Broadside');
var langList = new Array('Breton|||Breton', 'Catalan|||Catalan', 'Church Slavonic|||Church Slavonic', 'Croatian|||Croatian', 'Czech|||Czech', 'Danish|||Danish', 'Dutch|||Dutch', 'English|||English', 'Frisian|||Frisian', 'French|||French', 'German|||German', 'Greek|||Greek', 'Hebrew|||Hebrew', 'Italian|||Italian', 'Latin|||Latin', 'Portuguese|||Portuguese', 'Provencal / Occitan|||Proven\u00E7al / Occitan', 'Sardinian|||Sardinian', 'Spanish|||Spanish', 'Swedish|||Swedish');
var countryList = new Array('Balkans|||Balkans', 'Bohemia and Moravia|||Bohemia and Moravia', 'England|||England', 'France|||France (includes French-speaking Switzerland)', 'Germany|||Germany (includes German-speaking Switzerland, Austria & Alsace)', 'Hungary|||Hungary', 'Italy|||Italy', 'Low Countries|||Low Countries (includes towns under Burgundian rule)', 'Poland|||Poland', 'Portugal|||Portugal', 'Scandinavia|||Scandinavia', 'Spain|||Spain');
var locList = new Array('British Isles|||British Isles', 'Belgium|||Belgium', 'France|||France', 'Germany|||Germany', 'Italy|||Italy', 'Spain/Portugal|||Spain/Portugal', 'Netherlands|||Netherlands', 'U.S.A.|||U.S.A.', 'Other European|||Other European', 'Other|||Other', 'Doubtful|||Doubtful');

function changeInputs(iSelIdx, current){
	//put drop downs in if necessary
	
	if (iSelIdx == 8){	
		var formatDropDown = document.createElement('select')
		formatDropDown.setAttribute('id', 'fieldcont' + current);
		formatDropDown.setAttribute('name', 'fieldcont' + current);
		formatDropDown.setAttribute('style', 'width: 300');
		for (var i=0; i < formatList.length; i++){
			options = formatList[i].split('|||');			
			formatDropDown.options[i] = new Option(options[1],options[0]);
		}		
		var termfield = document.getElementById('fieldcont' + current);
		var parent = termfield.parentNode;
		var sibling = document.getElementById('fieldrel' + current);
		parent.removeChild(termfield);
		parent.insertBefore(formatDropDown, sibling);
	}
	else if (iSelIdx == 13){
		var langDropDown = document.createElement('select')
		langDropDown.setAttribute('id', 'fieldcont' + current);
		langDropDown.setAttribute('name', 'fieldcont' + current);
		langDropDown.setAttribute('style', 'width: 300');
		for (var i=0; i < langList.length; i++){
			options = langList[i].split('|||');			
			langDropDown.options[i] = new Option(options[1],options[0]);
		}
		var termfield = document.getElementById('fieldcont' + current);
		var parent = termfield.parentNode;
		var sibling = document.getElementById('fieldrel' + current);
		parent.removeChild(termfield);
		parent.insertBefore(langDropDown, sibling);
	}
	else if (iSelIdx == 4){
		var countryDropDown = document.createElement('select')
		countryDropDown.setAttribute('id', 'fieldcont' + current);
		countryDropDown.setAttribute('name', 'fieldcont' + current);
		countryDropDown.setAttribute('style', 'width: 300');
		for (var i=0; i < countryList.length; i++){
			options = countryList[i].split('|||');			
			countryDropDown.options[i] = new Option(options[1],options[0]);
		}
		var termfield = document.getElementById('fieldcont' + current);
		var parent = termfield.parentNode;
		var sibling = document.getElementById('fieldrel' + current);
		parent.removeChild(termfield);
		parent.insertBefore(countryDropDown, sibling);
	}
	else if (iSelIdx == 10){
		var locDropDown = document.createElement('select')
		locDropDown.setAttribute('id', 'fieldcont' + current);
		locDropDown.setAttribute('name', 'fieldcont' + current);
		locDropDown.setAttribute('style', 'width: 300');
		for (var i=0; i < locList.length; i++){
			options = locList[i].split('|||');			
			locDropDown.options[i] = new Option(options[1],options[0]);
		}
		var termfield = document.getElementById('fieldcont' + current);
		var parent = termfield.parentNode;
		var sibling = document.getElementById('fieldrel' + current);
		parent.removeChild(termfield);
		parent.insertBefore(locDropDown, sibling);
	}
	else {
		var textEntry = document.createElement('input');
		textEntry.setAttribute('type', 'text');
		textEntry.setAttribute('id', 'fieldcont' + current);
		textEntry.setAttribute('name', 'fieldcont' + current);
		textEntry.setAttribute('style', 'width: 300');
		var termfield = document.getElementById('fieldcont' + current);
		var value = termfield.value;
		var parent = termfield.parentNode;
		var sibling = document.getElementById('fieldrel' + current);		
		parent.removeChild(termfield);
		parent.insertBefore(textEntry, sibling);
		document.getElementById('fieldcont' + current).value = value;
	}
	
}

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
	if (iSelIdx != 4 && iSelIdx != 7 && iSelIdx != 8 && iSelIdx != 10 && iSelIdx != 13 && iSelIdx != 14) { var relationList = kwRelationList; }
	if (iSelIdx == 4 || iSelIdx == 7 || iSelIdx == 8 || iSelIdx == 10 || iSelIdx == 13 || iSelIdx == 14) { var relationList = exactRelationList; }
	if (iSelIdx == 11) {var relationList = dateRelationList; var rSelIdx = 2;}
	if (iSelIdx > 0 && relationList == kwRelationList) { var relationList = relationList.concat(proxRelationList); }
	if (iSelIdx == 0) { var relationList = kwRelationList.concat(phraseRelationList); }	
	
	// now replace existing relation select element
	relSelect.parentNode.insertBefore(createSelect('fieldrel' + current, relationList, rSelIdx), relSelect);
	relSelect.parentNode.removeChild(relSelect);
	
	//put in input option
	changeInputs(iSelIdx, current);

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
	if (iSelIdx != 7 && iSelIdx != 8 && iSelIdx != 13 && iSelIdx != 14) { var relationList = kwRelationList; }
	if (iSelIdx == 7 || iSelIdx == 8 || iSelIdx == 13 || iSelIdx == 14) { var relationList = exactRelationList; }
	if (iSelIdx == 11) {var relationList = dateRelationList; var rSelIdx = 2;}
	if (iSelIdx > 0 && relationList == kwRelationList) { var relationList = relationList.concat(proxRelationList); }
	if (iSelIdx == 0) { var relationList = kwRelationList.concat(phraseRelationList); }	
	
	//put in input option
//	changeInputs(iSelIdx, current);
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
	var selectElem = document.createElement('select');
	selectElem.id = name;
  	selectElem.name = name;
	for (var i=0; i < optionList.length; i++){
		var optionData = optionList[i].split('|||');
		var optionElem = document.createElement('option');
		optionElem.value = optionData[0];
		optionElem.innerHTML = optionData[1];
		
		if (i == selIdx) {optionElem.selected = 'selected'}
		selectElem.appendChild(optionElem);
	}
	return selectElem;
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
