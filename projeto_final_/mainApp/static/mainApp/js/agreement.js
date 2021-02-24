$(document).ready(function(){
    //agreement
    $("#agreementAcceptCheckbox").click(function() {
        if ($(this).prop("checked") == true) {
            $("#agreementAccept").prop("disabled", false);
        } else if ($(this).prop("checked") == false) {
            $("#agreementAccept").prop("disabled", true);
        }
    });
})