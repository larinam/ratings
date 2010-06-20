$(document).ready(function(){
    cmfLoadDocument();
});
function cmfLoadDocument() {
	$("a.fancybox").fancybox({
		'zoomSpeedIn':		300,
		'zoomSpeedOut':		300,
		'overlayShow':		false,
		"hideOnContentClick":true,
		"overlayShow":		true,
		"overlayOpacity":	0.5
	});
}