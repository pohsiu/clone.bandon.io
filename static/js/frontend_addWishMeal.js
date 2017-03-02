function submit() {
    var food=$("#wish_eat").val();
    var drink=$("#wish_drink").val();
    var id = $("#id").val();
    $.post(
        "/frontend/add_wish_meal",
        {id:id, food: food, drink: drink},
        function(response) {
          bootbox.alert({
              title: "許願池",
              message: response,
              });
        }
    );
    
        
    
}

