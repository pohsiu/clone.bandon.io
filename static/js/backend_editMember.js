function submit() {
    var pk=$("#pk").html();
    var name=$("#name").val();
    var phone=$("#phone").val();
    var email=$("#email").val();
    var category=$("#category").val();
    $.post(
        "/backend/editMember",
        {pk:pk, name: name, phone: phone, email: email, category: category},
        function(response) {
          alert(response);
        }
    );
}