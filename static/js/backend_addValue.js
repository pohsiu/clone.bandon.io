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
        $("#member option:first").attr('selected', 'selected');
        $("#member").selectpicker('refresh');
    });
});
function submit() {
    var member=$("#member").val();
    var value=$("#value").val();
    var admin=$("#admin").val();
    var comment=$("#comment").val();
    $.post(
        "addValue",
        {member: member, value: value, admin: admin, comment: comment},
        function(response) {
          alert(response);
        }
    );
}