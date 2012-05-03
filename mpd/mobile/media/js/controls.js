$(document).ready( function() {
    $('#connection').text("Connecting...");
    $('#content').show();
    // Connect to the mpd service
    connectEventHandlers();
    
    update();    
    setInterval( update, 1000 ); // Auto update the page
} );

function connectEventHandlers() {
    
    //Playback Buttons
    $('#prev').click( function() { $.get('/ajax/prev/'); } );
    $('#play').click( function() { $.get('/ajax/play/'); } );    
    $('#next').click( function() { $.get('/ajax/next/'); } );


    //Playback Settings
    $('#repeat').click( function() { 
        $.get('/ajax/repeat/', success=function() {
            $('#repeat').toggleClass('checked');
        } ); 
    } );
    $('#random').click( function() { 
        $.get('/ajax/random/', success=function() {
            $('#random').toggleClass('checked');
        } ); 
    } );
    $('#volume').change( function() {
        $.get('/ajax/volume/'+$(this).val() + '/' );
    } );
    
}

function update() {
    //Get current song information
    $.ajax( {
        url:'/ajax/status/', 
        success: function(data) {
            if( DEBUG ) { console.log( "Updating Status" ); }
            //Update the connection status, then hide it.
            $('#connection').text("Connected").slideUp('slow');
            
            data = $.parseJSON( data );
            
            data['position'] = toTime( data['elapsed'] ) + ' / ' + toTime( data['time'] )
            status = '#status'
            fields =  ['title', 'artist', 'album', 'position' ]
            for( i in fields) {
                tag = fields[ i ];
                //Make sure a element exists to hold the data
                if( !$(status).children(tag).length ) {
                    $(status).append('<p id="' + tag + '" class="oneLine"></p>');
                }
                
                //Place the data in the field
                $('#' + tag ).text( data[ tag ] );
            }
            
            //Update pause/play
            if( data['state'] == 'play' ) {
                $('#pause').show(); 
                $('play').hide();
            } else {
                $('#pause').hide();
                $('#play').show();
            }
            
            // Update Repeat
            if( data['repeat']  == '1' )
                $('#repeat').addClass( 'checked' );
            else
                $('#repeat').removeClass( 'checked' );
            
            // Update Random
            if( data['random']  == '1')
                $('#random').addClass( 'checked' );
            else
                $('#random').removeClass( 'checked' );
            
            // Update Volume
            $('#volume').val( data['volume'] );
            
            // Update Playlist Length
            $('#playlist').text( data['playlistlength'] );
            
            
            //Show the content
            $('#content').show();
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
