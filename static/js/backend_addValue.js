var categories;
var members;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
        // alert(JSON.stringify(members[0][0]));
        
        options="<option value='Z' select>選擇姓名</option>"
        for(var i=0; i<categories.length; i++) {
            options+="<option value='"+i+"'>"+categories[i].name+"</option>";
        }
        $("#category").html(options);
        
        $("#member").html("<option>選擇姓名</option>");
        $("#member").attr('disabled', true);
    });
    $("#category").change(function() {
        if ($(this).val() == 'Z') {
             $("#member").html("<option>選擇姓名</option>");
             $("#member").attr('disabled', true);
        }
        else {
            var brand = $(this).val();
            
            var options = '<option value="Z">選擇姓名</option>';
            for (var i = 0; i < members[brand].length; i++) {
                options += '<option value="' + members[brand][i].id + '">'  + members[brand][i].name + '</option>';
            }
            $("#member").html(options);
            $("#member option:first").attr('selected', 'selected');
            $("#member").attr('disabled', false);
        }
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