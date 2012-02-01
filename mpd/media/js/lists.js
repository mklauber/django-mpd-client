$(document).ready( function() {
    zebraRows('#list > li', 'odd');  
    
} );

function zebraRows(selector, className)  
{  
    $(selector).removeClass(className);
    $(selector+':even').addClass(className);  
}  
