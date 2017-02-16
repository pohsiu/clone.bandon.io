var shops;
var catalogs;
$( document ).ready(function() {
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
    var catalogs=$("#catalog").val();
    var drink=$("#drink").val();
    var dueDatetime=$("#dueDatetime").val();
    var id=$("#id").html();
    $.post(
        "/backend/editSchedule",
        {id: id, name: name, bandon: bandon, catalogs: catalogs, drink : drink, dueDatetime: dueDatetime},
        function(response) {
          alert(response);
        }
    );
}