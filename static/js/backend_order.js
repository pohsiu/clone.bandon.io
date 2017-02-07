function finish() {
    var pk=$("#pk").html();
    $.post(
        "finishSchedule",
        {pk: pk},
        function(response) {
          alert(response);
          window.location.href = "/backend/scheduleListPage";
        }
    );
}
