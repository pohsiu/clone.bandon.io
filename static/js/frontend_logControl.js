
function divclick(tableID){


    var table = $("#div"+tableID);
    var head = $("#head"+tableID);
    // console.log(table.html());
    table.animate({
        height:"toggle"    
    });
    $('html,body').animate({scrollTop: head.offset().top}, 500);

    
    
}

function logDivclick(tableID){

    
    
    var table = $("#logDiv"+tableID);
    var head = $("#logHead"+tableID);
    // console.log(table.html());
    table.animate({
        height:"toggle"    
    });
    $('html,body').animate({scrollTop: head.offset().top}, 500);

}