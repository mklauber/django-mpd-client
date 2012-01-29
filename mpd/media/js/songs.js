$(document).ready( function() {
    connectEventHandlers();
} );

function connectEventHandlers() {
    $('#songs tr:has(td)').click( function() {
        var row = $(this)
        // Prevent accidental double clicks
        if( $(this).is(':animated') ) { return; }
        // Show the highlight
        $(this).effect('highlight', { color : '#999999'}, 1000 );
        
        // Post the request
        var POST = [ $(this).attr('id') ];
        $.ajax( '/ajax/add/', {
            type: 'POST',   //As a post request
            data: {"songs": JSON.stringify( POST )}, //Post the song list
            success: function() {
                row.css('color', '#AAAAAA'); //If successful, change color of row
            },
            error: function() {
                //TODO Error handling here.
                //alert( "There was an error adding " + POST.length + " file(s) to the current playlist." );
            }
        } );
    } );
}
