
// Program:		keyboard.js
// Version:   	0.02
// Description:
//            	JavaScript functions for input of special characters into the ead template.  
//            	- produced for the Archives Hub v3.x. 
// Language:  	JavaScript
// Author(s):   John Harrison <john.harrison@liv.ac.uk>
//				Catherine Smith <catherine.smith@liv.ac.uk>
// Date:      	09/01/2009
// Copyright: 	&copy; University of Liverpool 2005-2009
//
// Version History:
// 0.01 - 08/08/2006 - JH - basic functions completed for original ead2002 template
// 0.02 - 09/01/2009 - CS - Addition of code to maintain current scroll position in text area after adding character
//							field codes changes to represent new ead editing interface




var	currentEntryField = null;
var	theFieldName = "Error. You have not yet selected a field to enter text into.";

var fieldMap = new Array();

	fieldMap['ISTCNo'] = 'ISTC Number - should not contain special characters';
	fieldMap['author'] = 'Author';
	fieldMap['title'] = 'Title';
	fieldMap['260_a'] = 'Imprints: Place';
	fieldMap['260_b'] = 'Imprints: Printer';
	fieldMap['260_c'] = 'Imprints: Date';
	fieldMap['format'] = 'Format';
	fieldMap['8_original'] = '008 Field: Original - should not contain special characters';
	fieldMap['8_date1'] = '008 Field: Date 1 - should not contain special characters';
	fieldMap['8_date2'] = '008 Field: Date 2 - should not contain special characters';
	fieldMap['8_lang'] = '008 Field: Language - should not contain special characters';		
	fieldMap['500_a'] = 'General Note';
	fieldMap['510_a'] = 'References: Reference';
	fieldMap['510_other'] = 'References: Other details';
	fieldMap['530_a'] = 'Reproduction Notes: Note';	
	fieldMap['530_u'] = 'Reproduction Notes: URL';
	fieldMap['holdings_a'] = 'Holdings: Library';
	fieldMap['holdings_b'] = 'Holdings: Details';
	fieldMap['852_a'] = 'British Library Shelfmark: Place';		
	fieldMap['852_q'] = 'British Library Shelfmark: Note';
	fieldMap['852_j'] = 'British Library Shelfmark: Shelfmark';
	fieldMap['internal_notes'] = 'Internal Notes';
	
			
	function getFieldName(code){
		if (code.indexOf('[') != -1){
			var lookup = code.replace(/\[[0-9]+\]/g, '');
		}
		else {
			var lookup = code;
		}
		return fieldMap[lookup];
	}
	
	function setCurrent(which) {
	  // onChange fires only when focus leaves, so use onFocus
	  if (which == 'none'){
	  	currentEntryField = null;
	  	theFieldName = "Error. You have not yet selected a field to enter text into.";
	  }
	  else {
	  	currentEntryField = which;
	  	theFieldName = getFieldName(which.id);
	  }
	}



function cursorInsert(field, insert) {
	/*
	// Description: a function to insert text at the cursor position in a specified field (textarea, text)
	*/
	if (insert == 'quot'){
		insert = '"';
	}
	if (field){
		//get scroll position
		var scrollPos = field.scrollTop;
		if (field.selectionStart || field.selectionStart == '0') {
			// Firefox 1.0.7, 1.5.0.6 - tested
			var startPos = field.selectionStart;
			var endPos = field.selectionEnd;
			if (endPos < startPos)	{
	          var temp = end_selection;
	          end_selection = start_selection;
	          start_selection = temp;
			}
			var selected = field.value.substring(startPos, endPos);
			field.value = field.value.substring(0, startPos) + insert + field.value.substring(endPos, field.value.length);
			//for FF at least we can get the curser to stay after the entered letter instead of at end of field
			//see http://www.scottklarr.com/topic/425/how-to-insert-text-into-a-textarea-where-the-cursor-is/ for possible improvements to IE version
			field.focus(); 
			field.selectionEnd = endPos + 1;
			field.selectionStart = endPos + 1;
		}
		else {
			 if (document.selection) {
				//Windows IE 5+ - tested
				field.focus();
				selection = document.selection.createRange();
				selection.text = insert;
			}
			else if (window.getSelection) {
				// Mozilla 1.7, Safari 1.3 - untested
				selection = window.getSelection();
				selection.text = insert;
			}
			else if (document.getSelection) {
				// Mac IE 5.2, Opera 8, Netscape 4, iCab 2.9.8 - untested
				selection = document.getSelection();
				selection.text = insert;
			} 
			else {
				field.value += insert;
			}
			field.focus(); //this puts cursor at end
		}
		//reset scroll to right place in text box
		if (scrollPos){
			field.scrollTop = scrollPos;
		}
	}
}
		
