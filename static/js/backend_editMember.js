function submit() {
    var id=$("#id").html();
    var name=$("#name").val();
    var phone=$("#phone").val();
    var email=$("#email").val();
    var category=$("#category").val();
    var admin;
    if($('#admin').prop('checked')) {
        admin=true;
    }
    else {
        admin=false
    }
    $.post(
        "/backend/editMember",
        {id:id, name: name, phone: phone, email: email, category: category, admin: admin},
        function(response) {
          alert(response);
        }
    );
}

function deleteMem() {
    var id=$("#id").html();
    if(confirm("Are you sure you want to delete?")) {
        $.post(
            "/backend/deleteMember",
            {id:id},
            function(response) {
              if(response=="saving") {
                  alert("Please return the saving.");
                  window.location.href="/backend/addValuePage";
              } else {
                  alert("Delete successfully.");
                  window.location.replace("/backend/memberListPage");
              }
            }
        );
    }
    else {
        alert("Cancel the deletion.");
    }
    
}