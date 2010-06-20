// url
function cmfRedirect(url) {
	if(url) {
		document.location.href = url;
		document.location = url;
	}
}
function cmfReload() {
	cmfRedirect(document.location.href);
}



// Window
function cmfOpenWindow(url, id, width, height) {
	//width = screen.width;
	//height = screen.height;

	window_top =(screen.height - height) / 2;
	window_left =(screen.width - width) / 2;
	w=window.open(url, id, 'width='+(width)+', height='+(height)+', top='+window_top+', left='+window_left+', toolbar=0, statusbar=0, location=0, scrollbars=no, resizable=0');
	w.focus();
	return false;
}
function cmfCloseWindow() {
	window.close();
}
function cmfOpenerUrl(url) {
    if(window.opener) {
		window.opener.document.location = url;
		window.close();
	} else {
	    cmfRedirect(url);
	}
}



// css
function cmfHideShow(id) {
	if(cmfIsHide(id)) {
		cmfShow(id);
		return true;
	} else {
		cmfHide();
		return false;
	}
}
function cmfHide(id) {
	if(typeof(id) == 'string') {
       id = '#'+ id;
	}
	$(id).addClass('cmfHide');
}
function cmfIsHide(id) {
	if(typeof(id) == 'string') {
       id = '#'+ id;
	}
	return $(id).hasClass('cmfHide');
}
function cmfShow(id) {
    if(typeof(id) == 'string') {
       id = '#'+ id;
	}
	$(id).removeClass('cmfHide');
}



// prefix chekbox
function cmfCheckboxPrefix(form, prefix, value) {
	var elements = form.elements;
	for(i=0; i<elements.length; i++)
		if(elements[i].id.indexOf(prefix)!=-1) elements[i].checked = value;
}

// text
function cmfTextFocus(id, value) {
	if(id.value==value) id.value = '';
}
function cmfTextOnblur(id, value) {
	if(id.value=='') id.value = value;
}



// point
function cmfGetId(id) {
	return document.getElementById(id);
}
function cmfGetValue(id) {
	return cmfGetId(id).value;
}
function cmfSetValue(id, value) {
	if(cmfGetId(id)) cmfGetId(id).value = value;
}



// Cookie
function cmfGetCookie(name) {
	var cookie = " " + document.cookie;
	var search = " " + name + "=";
	var setStr = null;
	var offset = 0;
	var end = 0;
	if (cookie.length > 0) {
		offset = cookie.indexOf(search);
		if (offset != -1) {
			offset += search.length;
			end = cookie.indexOf(";", offset)
			if (end == -1) {
				end = cookie.length;
			}
			setStr = unescape(cookie.substring(offset, end));
		}
	}
	return(setStr);
}