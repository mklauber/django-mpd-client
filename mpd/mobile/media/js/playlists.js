$(document).ready( function() {
    zebraRows('#songs > tbody tr', 'odd');
    connectEventHandlers();
    $('#songs tr').addClass('show');  
    
} );

function connectEventHandlers() {

    //Connect song table to ajax
    $('#songs tr >td:not(.delete)').click( function() {
        var song = $(this).parent().children('td').first().attr('id');

        $.get('/ajax/song/' + song + '/', 
        success=function() {
            window.location.href = '/'
        } ); 
    } );
    
    //Connect song table to ajax
    $('td.delete').click( function() {
        var row = $(this).parent();
        var song = row.children('td').first().attr('id');

        // Post the request
        var POST = [ row.children().first().attr('id') ];
        $.ajax( '/ajax/remove/', {
            type: 'POST',   //As a post request
            data: {"songs": JSON.stringify( POST )}, //Post the song list
            success: function() {
                // Show the highlight
                row.fadeOut( callback=function() { 
                    row.remove();
                    zebraRows('#songs > tbody tr', 'odd');                    
                } );
            },
            error: function() {
                //TODO Error handling here.
            }
        } );
    } );
    
    //Connect filter text box
    $('#filter').keyup( function() {
        if (event.keyCode == 27 || $(this).val() == '') {  
            //if esc is pressed we want to clear the value of search box  
            $(this).val('');

            //we want each row to be visible because if nothing  
            //is entered then all rows are matched.  
            $('#songs tr').addClass('show');
        }  
        query = $('#filter').val();
        
        $('#songs > tbody tr:has(td)').each( function() {
            $(this).text().search(new RegExp(query, "i")) < 0 ? $(this).removeClass("show") : $(this).addClass("show");
        } );
        $('#songs > tbody tr.show').removeClass('odd');  
        zebraRows('#songs > tbody tr.show', 'odd');  
    } );
    
    $('#clear').click( function() {
        // Post the request
        $.ajax( '/ajax/clear/', {
            type: 'POST',   //As a post request
            success: function() {
                $('#songs > tbody tr').remove();
            },
            error: function() {
                //TODO Error handling here.
                //alert( "There was an error adding " + POST.length + " file(s) to the current playlist." );
            }
        } );
    } );
    
    $('#save').click( function() {
    
        var name=prompt("Please enter your name", "");
        if ( name==null ) { return; }
        if ( name=="" ) { alert( "Name cannot be blank" ); return; }
        // Post the request
        $.ajax( '/ajax/save/', {
            type: 'POST',   //As a post request
            data: {"name": JSON.stringify( name )}, //Post the song list
            success: function() {
            
            },
            error: function() {
                //TODO Error handling here.
                //alert( "There was an error adding " + POST.length + " file(s) to the current playlist." );
            }
        } );
    } );
}

function zebraRows(selector, className)  
{  
    $(selector).removeClass(className);
    $(selector+':even').addClass(className);  
}  
