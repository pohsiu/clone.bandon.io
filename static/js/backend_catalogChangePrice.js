$( document ).ready(function() {
});
function submit() {
    if(confirm("Please be sure to adjust the price of all selected catalogs.")) {
        var catalog=$("#catalog").selectpicker('val');
        var price=$("#price").val();
        $.post(
            "/backend/catalogChangePrice",
            {catalog: catalog, price: price},
            function(response) {
              alert(response);
            }
        );
    }
}