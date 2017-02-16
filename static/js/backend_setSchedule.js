var shops;
var catalogs;
$( document ).ready(function() {
    document.getElementById("dueDatetime").value=nowString();
    
    var url = "/getShopCat";
    $.getJSON(url, function(res) {
        shops=res.shops;
        catalogs=res.catalogs;
    });
    $("#bandon").change(function() {
        $("#catalog option").remove();
        var shop = $(this).val();
        for (var i = 0; i < catalogs[shop].length; i++) {
            $("#catalog").append($("<option></option>").attr("value", catalogs[shop][i].id).text(catalogs[shop][i].name));
        }
        $("#catalog option:first").attr('selected', 'selected');
        $("#catalog").attr('disabled', false).selectpicker('refresh');
    });
});
function submit() {
    var name=$("#schedule_name").val();
    var bandon=shops[$("#bandon").val()].id;
    var drink=$("#drink").val();
    var dueDatetime=$("#dueDatetime").val();
    var catalogs=$("#catalog").selectpicker('val');
    if(Date.parse(dueDatetime)-1000*60*60*8<Date.now()) {
        alert("invalid time");
    } else {
        $.post(
            "/backend/setSchedule",
            {cata: catalogs, schedule_name: name, bandon : bandon, drink : drink, dueDatetime: dueDatetime},
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