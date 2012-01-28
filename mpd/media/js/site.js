var DEBUG = true;

function fixTopbarHiding() {
	var height = $('#topbar').height();
	$('#topbar').next().css("margin-top", "+="+height);
}

function fixBottombarHiding() {
	var height = $('#bottombar').height();
	$('#bottombar').prev().css("margin-bottom", "+="+height);
}

$(document).ready( function() {
    
	//Handle the Top Bar
	if ($('#topbar').length != 0) {
		fixTopbarHiding();
	}
	//Handle the bottom Bar
	if ($('#bottombar').length != 0) {
		fixBottombarHiding();
	}
	
	
} );

