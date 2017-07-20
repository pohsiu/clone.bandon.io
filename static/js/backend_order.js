function finish() {
    $('#finish').prop("disabled", true);
    $("#finish").remove();
    var id=$("#id").html();
    $.post(
        "/backend/finishSchedule",
        {id: id},
        function(response) {
          alert(response);
          window.location.href = "/backend/scheduleListPage/1/";
        }
    );
}

function arrive(type) {
    var id=$("#id").html();
    $('#'+type+'Arrived').prop("disabled", true);
    $.post(
        "/backend/"+type+"Arrive",
        {id: id},
        function(response) {
          alert(response);
          window.location.href = "/backend/order";
        }
    );
}
