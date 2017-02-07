var mark_list;
var member_list;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
        
        options="<option value='Z' select>選擇姓名</option>"
        for(var i=0; i<categories.length; i++) {
            options+="<option value='"+i+"'>"+categories[i].category_name+"</option>";
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
                options += '<option value="' + members[brand][i].pk + '">'  + members[brand][i].name + '</option>';
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
    var email=$("#email").val();
    var admin=$("#admin").val();
    var comment=$("#comment").val();
    // $.post(
    //     "addMember",
    //     {name: name, phone: phone, email: email, category: category},
    //     function(response) {
    //       alert(response);
    //     }
    // );
}