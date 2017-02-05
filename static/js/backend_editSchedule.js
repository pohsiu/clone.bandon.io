$( document ).ready(function() {
});
function submit() {
    var name=$("#schedule_name").val();
    var bandon=$("#bandon").val();
    var drink=$("#drink").val();
    var dueDatetime=$("#dueDatetime").val();
    var pk=$("#pk").html();
    $.post(
        "editSchedule",
        {pk: pk, schedule_name: name, bandon : bandon, drink : drink, dueDatetime: dueDatetime},
        function(response) {
          alert(response);
        }
    );
}
