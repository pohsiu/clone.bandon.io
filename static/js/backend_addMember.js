var categories;
var members;
$( document ).ready(function() {
    var url = "/getCateMem";
    $.getJSON(url, function(res) {
        categories=res.categories;
        members=res.members;
    });
});
function submit() {
    var name=$("#name").val();
    var sameName=false;
    var category="";
    for(var i=0; i<members.length; i++) {
        for(var j=0; j<members[i].length; j++) {
            if(name==members[i][j].name) {
                sameName=true;
                category=categories[i].name;
                break;
            }
        }
    }
    if(!sameName||(sameName&&confirm("same name with a person in "+category))) {
        var phone=$("#phone").val();
        var email=$("#email").val();
        var category=$("#category").val();
        $.post(
            "/backend/addMember",
            {name: name, phone: phone, email: email, category: category},
            function(response) {
              alert(response);
            }
        );
    }
}