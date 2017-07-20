
function submit() {
    var content= $("#btn-input").val();
    
    
    $('#submit').prop("disabled", true);
    $.post(
            "/backend/sendInstantMsg",
            {inputMsg:content},
            function(response) {
                alert(response);
            }
        );
    

    setTimeout(function(){
        $('#submit').prop("disabled", false);
    }, 300);
}