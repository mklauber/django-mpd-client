$(document).ready( function() {
	//Handle Radio Buttons
	$('.radio > *').click( function () {
		$(this).siblings().removeClass('checked');
		$(this).toggleClass('checked');
		
	} );

	// Handle Checkboxes
	$('.check > *').click( function () {
		$(this).toggleClass('checked');
		
	} );


	// Handle Toggle Switches
	$('.toggle').each( function() {
		if ( $(this).children('input[type=checkbox]').length )
		{
			$(this).children('input[type=checkbox]').addClass('toggleSwitch');
		} else {
			$(this).append('<input type="checkbox" class="toggleSwitch" />');
		}
	});
} );
