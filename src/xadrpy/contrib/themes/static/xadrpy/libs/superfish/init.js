$(document).ready(function(){ 
    $("ul.sf-menu").supersubs({ 
        minWidth:    12, 
        maxWidth:    27, 
        extraWidth:  1 
    }).superfish().find('ul').bgIframe({opacity:false});
});