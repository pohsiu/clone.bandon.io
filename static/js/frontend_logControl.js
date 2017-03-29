
function divclick(tableID){

    
    // var table = document.getElementById("div"+tableID);
    // console.log(table.style.display);
    var table = $("#div"+tableID);
    var head = $("#head"+tableID);
    // console.log(table.html());
    table.animate({
        height:"toggle"    
    });
    $('html,body').animate({scrollTop: head.offset().top}, 500);
    
    // if(table.style.display==="none"){
    //     table.style.display="block";
    //     // table.animate({
    //     //   top: '0px'
    //     // }, 1000);
    // }
    // else{
    //     table.style.display="none";
    //     // table.animate({
    //     //   top: '-100px'
    //     // }, 1000);
        
    // }
}