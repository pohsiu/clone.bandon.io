var categories;
var members;
$( document ).ready(function() {
    var url = "/getShopCat";
    $.getJSON(url, function(res) {
        shops=res.shops;
        catalogs=res.catalogs;
    });
    $("#shop").change(function() {
        var shop = $(this).val();
        
        $("#catalog option").remove();
        for (var i = 0; i < catalogs[shop].length; i++) {
            $("#catalog").append($("<option></option>").attr("value", catalogs[shop][i].id).text(catalogs[shop][i].name));
        }
        $("#catalog option:first").attr('selected', 'selected');
        $("#catalog").selectpicker('refresh');
    });
});
function submit() {
    if(confirm("sure to set all orders to this bandon?")) {
        var catalog=$("#catalog").val();
        $.post(
            "/backend/emergency",
            {catalog: catalog},
            function(response) {
              alert(response);
            }
        );
    }
}