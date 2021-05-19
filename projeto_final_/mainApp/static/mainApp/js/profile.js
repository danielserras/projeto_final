$(document).ready(function () {
    //Define min in highest value
    $("#minProfile").on('input', function() {
        $("#maxProfile").attr("min", $("#minProfile").val());
    });
    //Define max in lowest value
    $("#maxProfile").on('input', function() {
        if($("#maxProfile").val() >= 2000){
            $("#minProfile").attr("max", 2000);
        }
        else{
            $("#minProfile").attr($("#maxProfile").val())
        }
    });
});

function showDeleteAccountPopUp() {
    $('#modalDeleteAccount').modal('show');
    $(".deletePOP").click(function() {
        $('#modalDeleteAccount').modal('hide');
    });
}

function browseFile(div){
    div.parentElement.childNodes[1].click();
}

function upload_img(input) {
    if (input.files && input.files[0]) {
        $("#btnSaveProfileChanges").click();
    }
}