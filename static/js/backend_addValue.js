var categories;
var members;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
    });
    $("#category").change(function() {
        var cate = $(this).val();
        
        $("#member option").remove();
        for (var i = 0; i < members[cate].length; i++) {
            $("#member").append($("<option></option>").attr("value", members[cate][i].id).text(members[cate][i].name));
        }
        $("#saving").html(members[cate][0].saving);
        $("#member option:first").attr('selected', 'selected');
        $("#member").selectpicker('refresh');
    });
    $("#member").change(function() {
        var cate = $("#category").val();
        var saving=0;
        for (var i = 0; i < members[cate].length; i++) {
            if(members[cate][i].id==$(this).val())
                saving=members[cate][i].saving
        }
        $("#saving").html(saving);
    });
});

function submit() {
    $('#submit').prop("disabled", true);
    var member=$("#member").val();
    var value=$("#value").val();
    var admin=$("#admin").val();
    var comment=$("#comment").val();
    $.post(
        "/backend/addValue",
        {member: member, value: value, admin: admin, comment: comment},
        function(response) {
          alert(response);
          var newSaving=parseInt($("#saving").html())+parseInt(value);
          $("#saving").html(newSaving);
          $("#value").val(0);
        }
    );

    setTimeout(function(){
        $('#submit').prop("disabled", false);
    }, 300);
}