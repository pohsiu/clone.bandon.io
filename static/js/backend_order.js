function finish() {
    $("#finish").remove();
    var id=$("#id").html();
    $.post(
        "/backend/finishSchedule",
        {id: id},
        function(response) {
          alert(response);
          window.location.href = "/backend/scheduleListPage";
        }
    );
}

function arrive() {
    var id=$("#id").html();
    $.post(
        "/backend/arriveSchedule",
        {id: id},
        function(response) {
          alert(response);
          window.location.href = "/backend/order";
        }
    );
}
