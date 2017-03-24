
function divclick(tableID){

    
    var table = document.getElementById("div"+tableID);
    // console.log(table.style.display);
    // var table = $("#div"+tableID);
    // console.log(table.html());
    if(table.style.display==="none"){
        table.style.display="block";
        // table.animate({
        //   top: '0px'
        // }, 1000);
    }
    else{
        table.style.display="none";
        // table.animate({
        //   top: '-100px'
        // }, 1000);
        
    }
}