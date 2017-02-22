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
        $("#price").val(catalogs[shop][0].price);
        $("#catalog option:first").attr('selected', 'selected');
        $("#catalog").selectpicker('refresh');
    });
    $("#catalog").change(function() {
        var shop = $("#shop").val();
        for (var i = 0; i < catalogs[shop].length; i++) {
            if(catalogs[shop][i].id==$(this).val())
                $("#price").val(catalogs[shop][i].price);
        }
        
    });
});
function submit() {
    var catalog=$("#catalog").val();
    var price=$("#price").val();
    var influence=$("#influence").prop('checked');
    $.post(
        "/backend/catalogChangePrice",
        {catalog: catalog, price: price, influence: influence},
        function(response) {
          alert(response);
        }
    );
}