$(document).ready(function() {
    //agreement
    $("#agreementAccept").click(function(){
        if($(this).prop("checked") == true){
            $("#agreementSubmit").prop("disabled", false);
        }
        else if($(this).prop("checked") == false){
            $("#agreementSubmit").prop("disabled", true);
        }
    })

});