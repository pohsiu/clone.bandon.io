function orderForm() {
    var $form = $('#orderForm');
    var btn = $form.find('input[type=submit]');
    btn.prop("disabled", true);
    
    var member_id = document.forms["orderform"]["member_id"].value;
    var foodlen = document.forms["orderform"]["food-len"].value;
    var schedule_id = document.forms["orderform"]["schedule_id"].value;
    var lock = 0;
    var drinkname = document.forms["orderform"]["drink-name"].value;
    var drinkprice = document.forms["orderform"]["drink-price"].value;
    var sugar = document.forms["orderform"]["sugar"].value;
    var ice = document.forms["orderform"]["ice"].value;
    var drinkcomment = document.forms["orderform"]["drink-comment"].value;
    
    var strindex;
    var food_num;
    var foodJson=[];
    
    
    
    for (var i = 1; i <= foodlen; i++) {
        strindex = i.toString();
        food_num = document.forms["orderform"]["food-num"+strindex].value;
       
        if(food_num != "0"){
            lock = 1;
        }
    }
    
    
    
    if (drinkname == "" && lock == 0) {
        bootbox.alert({
            title:"訂餐失敗",
            message:"請選擇餐點"
        });
        recover();
        
        return false;
    }
    else if (drinkname != "" && drinkprice ==""){
        bootbox.alert({
            title:"訂餐失敗",
            message:"請輸入飲料價格"
        });
        recover();
        return false;
    }
    else{
        $.post(
          "/frontend/check_order",
          {schedule_id:schedule_id,member_id:member_id},
          function(response) {
              if(response == "insufficient"){
                  bootbox.alert({
                    title:"<h3 style='color:#0C182D; font-weight:bold;'>請儲值</h3>",
                    message: "<h4>您的帳戶餘額不足，請儲值後再進行點餐</h4>",
                    backdrop: true
                    });
              }
              else if(response == "both"){
                  bootbox.confirm({
                        title: "訂餐確認",
                        message: "您已經有訂飲料跟便當了，確定加點嗎?",
                        buttons: {
                            cancel: {
                                label: '取消',
                                className: 'btn-danger'
                            },
                            confirm: {
                                label: '確定',
                                className: 'btn-success'
                            }
                        },
                        callback: function (result) {
                            if(result==true){
                                post();
                            }
                            else{
                                recover();
                            }
                            console.log('This was logged in the callback: ' + result);
                        }
                    });
              }
              else if(response == "food"){
                  bootbox.confirm({
                        title: "訂餐確認",
                        message: "您已經有訂便當了，確定加點嗎?",
                        buttons: {
                            cancel: {
                                label: '取消',
                                className: 'btn-danger'
                            },
                            confirm: {
                                label: '確定',
                                className: 'btn-success'
                            }
                        },
                        callback: function (result) {
                            if(result==true){
                                post();
                            }
                            else{
                                recover();
                            }
                            console.log('This was logged in the callback: ' + result);
                        }
                    });
              }
              else if(response == "drink"){
                  bootbox.confirm({
                        title: "訂餐確認",
                        message: "您已經有訂飲料了，確定加點嗎?",
                        buttons: {
                            cancel: {
                                label: '取消',
                                className: 'btn-danger'
                            },
                            confirm: {
                                label: '確定',
                                className: 'btn-success'
                            }
                        },
                        callback: function (result) {
                            if(result==true){
                                post();
                            }
                            else{
                                recover();
                            }
                            console.log('This was logged in the callback: ' + result);
                        }
                    });
              }
              else{
                  post();
              }
          }
        );
        
        return false;
    }
    function post(){
        var foodlist=[]
        for (var i = 1; i <= foodlen; i++) {
            catalog_id = document.forms["orderform"]["catalog-id"+i].value;
            food_num = document.forms["orderform"]["food-num"+i].value;
            food_name = document.forms["orderform"]["food-name"+i].value;
            foodJson.push({catalog_id:catalog_id , food_num:food_num});
            foodlist.push({name:food_name, num:food_num});
        }
        
        $.post(
            "/frontend/add_order",
            {foodJson:JSON.stringify(foodJson), drinkname:drinkname, drinkprice:drinkprice, member_id:member_id, schedule_id:schedule_id, sugar:sugar, ice:ice, drinkcomment:drinkcomment },
            function(response) {
            var cart = "";
            // console.log(foodlist[0]);
            // console.log(JSON.parse(foodlist[0].num));
            // console.log(foodlist.length);
            
            for(var listi = 0; listi< foodlist.length; listi++){
                if(JSON.parse(foodlist[listi].num) != "0"){
                    cart= cart+JSON.stringify(foodlist[listi].name)+" "+JSON.parse(foodlist[listi].num)+"個<br>";
                }
            }
            console.log(cart);
            bootbox.alert({
                title: "訂餐結果",
                message: response+"</br>"+cart+drinkname,
                callback: function () {
                    console.log('This was logged in the callback!');
                    document.forms["orderform"].remove();
                    window.location.replace("/todayOrder/"+member_id+"/");
                }
                });
            }
        );
    }
    function recover(){
        setTimeout(function(){
            btn.prop("disabled", false);
        }, 300);
    }
    
}
