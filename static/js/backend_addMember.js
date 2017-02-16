function submit() {
    var name=$("#name").val();
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