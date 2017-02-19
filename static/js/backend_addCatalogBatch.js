function submit() {
    if (confirm("Please make sure your input is valid.")) {
        var shop=$("#foodShop").val();
        var input=$("#input").val()
        if(checkValid(input)) {
            $.post(
                "/backend/addCatalogBatch",
                {shop: shop, input: input},
                function(response) {
                  alert(response);
                  window.location.href="/backend/catalogListPage/";
                }
            );
        } else {
            alert('not valid input');
        }
    }
}

function checkValid(input) {
    lines=input.split('\n')
    for(var i in lines) {
        cleanLine=$.trim(lines[i]);
        temp=cleanLine.split(' ');
        if(temp.length==2) {
            name=temp[0];
            price=temp[1];
            if(isNaN(price)) {
                return false;
            }
        } else {
            return false;
        }
    }
    return true;
}