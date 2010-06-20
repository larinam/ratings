function cmfShowSearch() {
	$('.fastSearch2').each(function() {
         cmfHide(this);
	});
	$('.fastSearch1').each(function() {
         cmfShow(this);
	});
	return false;
}
function cmfHideSearch() {
	$('.fastSearch1').each(function() {
         cmfHide(this);
	});
	$('.fastSearch2').each(function() {
         cmfShow(this);
	});
	return false;
}

function cmfSelectBrandAll() {
	$('input[type=checkbox]', $('.check', $('.checkDivBrand'))).each(function() {
         this.checked = cmfGetId('checkBrandAll').checked;
	});
}

function changeBrandOfSection($sec) {
	return cmfAjaxSend(jsControllerUrl +'/catalog/sectionBrand.php', {section: $sec});
}

function changeMainBrandOfSection($sec) {
	return cmfAjaxSend(jsControllerUrl +'/catalog/sectionBrand.php', {section: $sec, main: 1});
}

function searchDefaultForm(text, id) {
    search = cmfGetValue(id);
    if(!search) {
    	cmfSetValue(id, text);
    }
    return false;
}

function searchSmallChangeMain(count) {
	if(count>4) count = 4;
	css1 = 'mag_search_'+ count + '_main1';
	css2 = 'mag_search_'+ count + '_main2';

	if(cmfIsHide('mainSearchText')) {
  		$('#mainSearchA').html('обычный поиск');
        cmfShow('mainSearchText');
        $('#mainSearchDiv').removeClass('mag_search_small1');
        $('#mainSearchDiv').addClass(css1);
        $('#mainSearchDiv > div').removeClass('mag_search_small2');
        $('#mainSearchDiv > div').addClass(css2);
	} else {
        $('#mainSearchA').html('расширенный поиск');
        cmfHide('mainSearchText');
        $('#mainSearchDiv').removeClass(css1);
        $('#mainSearchDiv').addClass('mag_search_small1');
        $('#mainSearchDiv > div').removeClass(css2);
        $('#mainSearchDiv > div').addClass('mag_search_small2');
	}
}


function cmfShangeMainImage(count) {
    if(count>0) {
	    document.countShopMain = count;
    } else {
    	if(!document.countShopMain) document.countShopMain = 1;
    	count = document.countShopMain + (count==-1 ? -1 : 1);
    }
    if(count) {
    	cmfAjaxSend(jsControllerUrl +'/catalog/shop.php', {count: count});
    }
    return false;
}




function cmfCatalogSelectImage(parent) {
	//var parent = tag.parentNode;
	var id = parent.id.replace('list', '');

	if(document.SelectImage==id) return false;
	document.SelectImage = id;


	var imageMain = $('#imageMain').attr('src');
	$('#imageMain').attr('src', $('#image'+id).attr('src'));
	$('#image'+id).attr('src', imageMain);

	var listMain = $('#listMain').attr('src');
	$('#listMain').attr('src', $('#list'+id).attr('src'));
	$('#list'+id).attr('src', listMain);

	return false;
}

function cmfCatalogSelectImageOver() {
	setTimeout("cmfCatalogSelectImageOver2();", 500);
	return false;
}
function cmfCatalogSelectImageOver2() {
	document.SelectImage = '';
	return false;
}

function cmfProductMenu(id) {
    switch(id) {
    	 case 'articleList':
    	 	cmfHide('commentList');
    	 	cmfHide('paramList');
    	 	cmfShow('articleList');
    	 	break;

    	 case 'paramList':
    	 	cmfHide('articleList');
    	 	cmfHide('commentList');
    	 	cmfShow('paramList');
    	 	break;

    	 case 'commentList':
    	 	cmfHide('articleList');
    	 	cmfHide('paramList');
    	 	cmfShow('commentList');
    	 	break;
    }
    return false;
}

function cmfProductArticleList(param, page) {
    param.page = page;
    return cmfAjaxSend(jsControllerUrl +'/catalog/productArticle.php', param);
}


function cmfSectionFilterShange(form) {
	return cmfAjaxSend(jsControllerUrl +'/catalog/filter.php', form);
}