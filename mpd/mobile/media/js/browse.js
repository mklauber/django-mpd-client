$(document).ready( function() {
    $('#connection').text("Connecting...");
    $('#content').show();
    // Connect to the mpd service
    connectEventHandlers();
    
    update();    
    setInterval( update, 5000 ); // Auto update the page
} );

function connectEventHandlers() {
    
    //Playback Buttons
    $('#update').click( function() { 
		if( !$(this).data("in-progress") ) { 
			$.get('/ajax/update/'); 
			$('#update').data("in-progress", true).text("Updating...");
		} 
	} );
}

function update() {
    //Get current song information
    $.ajax( {
        url:'/ajax/status/', 
        success: function(data) {
            
            data = $.parseJSON( data );
            
            //Are we currently updating
            if( 'updating_db' in data ) {
                $('#update').data("in-progress", true).text("Updating...");
            } else {
                $('#update').data("in-progress", false).text("Update");
            }
            
            $('#search > span').text(data['songs']);
            $('#artists > span').text(data['artists']);
            $('#albums > span').text(data['albums']);
            $('#songs > span').text(data['songs']);
        },
        //Handle a 500 error
        error: function(xhr, ajaxOptions, thrownError) {
        
            $('#connection').text('Error connecting... trying again').slideDown('fast');
        }
    } );
}

// Helper Functions

//Convert a given number of seconds to a formatted time.  Does not handle hours.
function toTime( seconds ) {
	if( !isNumber( seconds ) )
		return '0:00';
    var secs = Math.floor( seconds % 60 )
    return Math.floor( seconds / 60 ) + ':' + ( ( secs + "").length < 2 ? ('0' + secs ) : secs );
}

function isNumber( n ) {
	return !isNaN( parseFloat( n ) ) && isFinite( n );
}
