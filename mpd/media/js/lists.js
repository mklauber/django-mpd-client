$(document).ready( function() {
    zebraRows('#list > li', 'odd'); 
    $('#list > li').addClass('show');
    
    
    //Connect filter text box
    $('#filter').keyup( function() {
        if (event.keyCode == 27 || $(this).val() == '') {  
            //if esc is pressed we want to clear the value of search box  
            $(this).val('');

            //we want each row to be visible because if nothing  
            //is entered then all rows are matched.  
            $('#list > li').addClass('show');  
        }  
        query = $('#filter').val();
        
        $('#list > li').each( function() {
            $(this).text().search(new RegExp(query, "i")) < 0 ? $(this).removeClass("show") : $(this).addClass("show");
        } );
        $('#list > li').removeClass('odd');  
        zebraRows('#list > li.show', 'odd');  
    } );
} );

function zebraRows(selector, className)  
{  
    $(selector).removeClass(className);
    $(selector+':even').addClass(className);  
}  
