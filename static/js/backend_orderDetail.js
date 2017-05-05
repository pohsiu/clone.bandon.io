var categories;
var members;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
    });
    $("#category-food").change(function() {
        var cate = $(this).val();
        
        $("#member-food option").remove();
        for (var i = 0; i < members[cate].length; i++) {
            $("#member-food").append($("<option></option>").attr("value", members[cate][i].id).text(members[cate][i].name));
        }
        $("#member-food option:first").attr('selected', 'selected');
        $("#member-food").selectpicker('refresh');
    });
    $("#category-drink").change(function() {
        var cate = $(this).val();
        
        $("#member-drink option").remove();
        for (var i = 0; i < members[cate].length; i++) {
            $("#member-drink").append($("<option></option>").attr("value", members[cate][i].id).text(members[cate][i].name));
        }
        $("#member-drink option:first").attr('selected', 'selected');
        $("#member-drink").selectpicker('refresh');
    });
});

function deleteFoodOrder(id) {
    if(confirm("sure to delete?")) {
        $.post(
            "/backend/deleteFoodOrder",
            {orderId: id},
            function(response) {
                if(response) {
                    $("#food"+id).remove();
                    var count=$("#foodCount"+response.bag).html();
                    count=parseInt(count)-response.count;
                    $("#foodCount"+response.bag).html(count);
                    
                    var price=$("#foodPrice").html();
                    price=parseInt(price)-response.price;
                    $("#foodPrice").html(price);
                } else {
                    alert("Schedule is finished.");
                }
            }
        );
    }
}

function deleteDrinkOrder(id) {
    if(confirm("sure to delete?")) {
        $.post(
            "/backend/deleteDrinkOrder",
            {orderId: id},
            function(response) {
                if(response) {
                    $("#drink"+id).remove();
                    var count=$("#drinkCount"+response.bag).html();
                    count=parseInt(count)-response.count;
                    $("#drinkCount"+response.bag).html(count);
                    
                    var price=$("#drinkPrice").html();
                    price=parseInt(price)-response.price;
                    $("#drinkPrice").html(price);
                } else {
                    alert("Schedule is finished.");
                }
            }
        );
    }
}

function addFoodOrder() {
    var member=$("#member-food").val();
    var catalog=$("#catalog").val();
    var count=$("#count-food").val();
    
    $.post(
        "/backend/addFoodOrder",
        {member: member, catalog: catalog, count: count},
        function(response) {
            if(response) {
                var bag=response.bag;
                var row='\
                        <tr id="food'+response.id+'">\
                            <td>'+response.remark+'</td>\
                            <td>'+response.member+'</td>\
                        	<td>'+response.catalog+'</td>\
                            <td>'+response.count+'</td>\
                            <td>'+response.price+'</td>\
                            <td><a onclick="deleteFoodOrder('+response.id+');"><span class="glyphicon glyphicon-remove" style="cursor: pointer;"></span></a></td>\
                        </tr>'
                if(bag!=3) {
                    $("#foodBag"+(bag+1)).before(row);
                } else {
                    $("#food").append(row);
                }
                
                var count=$("#foodCount"+response.bag).html();
                count=parseInt(count)+response.count;
                $("#foodCount"+response.bag).html(count);
                
                var price=$("#foodPrice").html();
                price=parseInt(price)+response.price;
                $("#foodPrice").html(price);
            } else {
                alert("Schedule is finished.");
            }
        }
    );
}

function addDrinkOrder() {
    var member=$("#member-drink").val();
    var drink=$("#drink").val();
    var remark=$("#sugar").val()+$("#ice").val()+$("#comment").val();
    var price=$("#price").val();
    $.post(
        "/backend/addDrinkOrder",
        {member: member, drink: drink, remark: remark, price: price},
        function(response) {
            if(response) {
                var bag=response.bag;
                var row='\
                        <tr id="drink'+response.id+'">\
                            <td>'+response.remark+'</td>\
                            <td>'+response.member+'</td>\
                        	<td>'+response.drink+'</td>\
                        	<td>'+response.remark+'</td>\
                            <td>'+response.count+'</td>\
                            <td>'+response.price+'</td>\
                            <td><a onclick="deleteDrinkOrder('+response.id+');"><span class="glyphicon glyphicon-remove" style="cursor: pointer;"></span></a></td>\
                        </tr>'
                if(bag!=3) {
                    $("#drinkBag"+(bag+1)).before(row);
                } else {
                    $("#drink").append(row);
                }
                
                var count=$("#drinkCount"+response.bag).html();
                count=parseInt(count)+1;
                $("#drinkCount"+response.bag).html(count);
                
                var price=$("#drinkPrice").html();
                price=parseInt(price)+response.price;
                $("#drinkPrice").html(price);
            } else {
                alert("Schedule is finished.");
            }
        }
    );
}