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
function recommendSubmit() {
    var food=$("#textfood").val();
    var drink=$("#textdrink").val();
    var id = $("#id").val();
    if(food=='' && drink==''){
        bootbox.alert({
            title: "許願失敗",
            message: "不要鬧了，您什麼都沒打阿",
        });
    }
    else{
        $.post(
            "/frontend/add_text_meal",
            {id:id, food: food, drink: drink},
            function(response) {
              bootbox.alert({
                  title: "許願池",
                  message: response,
                  });
            }
        );
    }
        
    
}

