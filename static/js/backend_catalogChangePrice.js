var catalogs;
$( document ).ready(function() {
    var url = "/getScheduleCatalogs";
    $.getJSON(url, function(res) {
        catalogs=res.catalogs;
    });
    $("#catalog").change(function() {
        for (var i = 0; i < catalogs.length; i++) {
            if(catalogs[i].id==$(this).val())
                $("#price").val(catalogs[i].price);
        }
    });
});
function submit() {
    var catalog=$("#catalog").val();
    var price=$("#price").val();
    $.post(
        "/backend/catalogChangePrice",
        {catalog: catalog, price: price},
        function(response) {
          alert(response);
        }
    );
}