function finish() {
    var id=$("#id").html();
    $.post(
        "finishSchedule",
        {id: id},
        function(response) {
          alert(response);
          window.location.href = "/backend/scheduleListPage";
        }
    );
}
