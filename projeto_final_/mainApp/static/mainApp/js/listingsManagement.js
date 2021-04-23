$(document).ready(function () {
    $(".isActive").change(function (e) { 
        e.preventDefault();
        $(this).parent()[0].submit();
    });

    $("#close_delete_agreement_modal").click(function(){
        $("#delete_agreement_modal").modal("hide");
    })
});