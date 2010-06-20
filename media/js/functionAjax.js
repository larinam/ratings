// передать запрос с формой, не кешировать его
function cmfAjaxSendForm(form, url) {
	return cmfAjaxSend(url, { form: form }, false, false);
}
// передать запрос с данными и закешировать его
function cmfAjaxSendCache(url, value, func) {
	return cmfAjaxSend(url, value, func, true);
}
// отправить запрос по адресу в определенную функцию с заданными данными
function cmfAjaxSend(url, value) {
    var req = new JsHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
			if(req.responseText) {
	            if($.browser.msie && $.browser.version=='6.0') {
	            } else {
	            	cmfAjaxLog(req.responseText);
	            }
            }

			if(req.responseJS && req.responseJS.loadHTML) {
				$(req.responseJS.loadHTML).each(function() {

					$(this.id).html(this.content);
				});
			}
			if(req.responseJS && req.responseJS.js) $.globalEval(req.responseJS.js);
            //cmfLoadDocument();
        }
    }
    req.open(null, url, true);
    req.send(value);
    return false;
}

// вывести лог запроса
function cmfAjaxLog(text) {
	$('#idAjaxLog').show();
	$('#idAjaxLog').html(text);
}

// выполнение ajax команды
function cmfAjaxCommand(url) {
	$('#idAjaxCommand2').html('<iframe src="'+ url +'" width="100%" height="1000px" scrolling="yes" frameborder="0"></iframe>');
	$('#idAjaxCommand1').show();
}