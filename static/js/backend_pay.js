var categories;
var members;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
    });
    $("#categoryReceive").change(function() {
        var cate = $(this).val();
        
        $("#memberReceive option").remove();
        for (var i = 0; i < members[cate].length; i++) {
            $("#memberReceive").append($("<option></option>").attr("value", members[cate][i].id).text(members[cate][i].name));
        }
        $("#memberReceive option:first").attr('selected', 'selected');
        $("#memberReceive").selectpicker('refresh');
    });
    $("#categoryPay").change(function() {
        var cate = $(this).val();
        
        $("#memberPay option").remove();
        for (var i = 0; i < members[cate].length; i++) {
            $("#memberPay").append($("<option></option>").attr("value", members[cate][i].id).text(members[cate][i].name));
        }
        $("#memberPay option:first").attr('selected', 'selected');
        $("#memberPay").selectpicker('refresh');
    });
});

function submit() {
    $('#submit').prop("disabled", true);
    var memberReceive=$("#memberReceive").val();
    var memberPay=$("#memberPay").val();
    var value=$("#value").val();
    var admin=$("#admin").val();
    var comment=$("#comment").val();
    $.post(
        "/backend/chuChienPay",
        {memberReceive: memberReceive, memberPay: memberPay, value: value, admin: admin, comment: comment},
        function(response) {
          alert(response);
        }
    );

    setTimeout(function(){
        $('#submit').prop("disabled", false);
    }, 300);
}