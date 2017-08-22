var shops;
var catalogs;
$( document ).ready(function() {
    document.getElementById("dueDatetime").value=timeString();
    
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
    $('#submit').prop("disabled", true);
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

function timeString() {
    var now=new Date();
    var month=now.getMonth()>8?"":"0"+(now.getMonth()+1);
    var date=now.getDate()>9?"":"0"+now.getDate();
    var hour="09";
    var minute="40";
    var nowString=now.getFullYear()+'-'+month+'-'+date+'T'+hour+':'+minute;
    return nowString
}