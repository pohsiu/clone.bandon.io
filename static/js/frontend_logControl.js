
function divclick(tableID){

    
    var table = document.getElementById("div"+tableID);
    console.log(table.style.display);
    if(table.style.display==="none"){
        table.style.display="block";
    }
    else{
        table.style.display="none";
    }
}