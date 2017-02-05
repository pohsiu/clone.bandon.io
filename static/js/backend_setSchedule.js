$( document ).ready(function() {
    document.getElementById("dueDatetime").value=nowString();
});
function submit() {
    var name=$("#schedule_name").val();
    var bandon=$("#bandon").val();
    var drink=$("#drink").val();
    var dueDatetime=$("#dueDatetime").val();
    if(Date.parse(dueDatetime)-1000*60*60*8<Date.now()) {
        alert("invalid time");
    } else {
        $.post(
            "setSchedule",
            {schedule_name: name, bandon : bandon, drink : drink, dueDatetime: dueDatetime},
            function(response) {
              alert(response);
            }
        );
    }
}

function nowString() {
    var now=new Date();
    var offset1=now.getMonth()>8?"":"0";
    var offset2=now.getDate()>9?"":"0";
    var offset3=now.getHours()>9?"":"0";
    var offset4=now.getMinutes()>9?"":"0";
    var nowString=now.getFullYear()+'-'+offset1+(now.getMonth()+1)+'-'+offset2+now.getDate()+'T'+offset3+now.getHours()+':'+offset4+now.getMinutes();
    return nowString
}