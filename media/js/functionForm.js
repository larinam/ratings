/* select */
function cmfSelectChildDelete(selectObj) {
	while (selectObj.childNodes.length) {
		if (selectObj.firstChild.tagName == 'optgroup') {
			while (selectObj.firstChild.childNodes.length)
				selectObj.firstChild.removeChild(selectObj.firstChild.firstChild);
		}
		selectObj.removeChild(selectObj.firstChild);
	}
}

function cmfSelectOption(parent, text, value, selected, selected2) {
	parent.options.add(new Option(text,value,selected,selected2));
	return parent.lastChild;
}
function cmfSelectOptgroup(parent, text, value, selected, selected2) {
	var opt1 = new Option(text,value,selected,selected2);
	parent.appendChild(opt1);
	opt1.text = text;
	opt1.value = value;
	return opt1;
}



function cmfFormNoError(id) {
	$(id.previousSibling).html('');
	$(id.previousSibling).attr('class', 'errorDiv');
}


function cmfFormTextSelectLabel(id) {
    cmfGetId(id).focus();
    cmfGetId(id).select();
}