function deleteFoodOrder(id) {
    if(confirm("sure to delete?")) {
        $.post(
            "/backend/deleteFoodOrder",
            {orderId: id},
            function(response) {
                if(response=="True") {
                    $("#food"+id).remove();
                } else {
                    alert("Schedule is finished.")
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
                if(response=="True") {
                    $("#drink"+id).remove();
                } else {
                    alert("Schedule is finished.")
                }
            }
        );
    }
}