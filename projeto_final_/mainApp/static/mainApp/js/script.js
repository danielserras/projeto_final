$(document).ready(function() {
    //Hide advanced search
    $('#advancedSearchDiv').toggle('invisible');
    //agreement
    $("#agreementAccept").click(function() {
        if ($(this).prop("checked") == true) {
            $("#agreementSubmit").prop("disabled", false);
        } else if ($(this).prop("checked") == false) {
            $("#agreementSubmit").prop("disabled", true);
        }
    });
    //Show/Hide advanced search at button press
    document.querySelector('.advancedSearchFormButton').addEventListener('click', function() {
        $('#advancedSearchDiv').toggle('invisible');
        this.classList.toggle('rotated');

        /*divElem = document.getElementById("advancedSearchDiv");
        //divElem.style.visibility = "hidden";
        console.log(divElem.style.visibility);
        if (divElem.style.visibility === "hidden") {
            divElem.style.visiblity = "visible";
        } else {
            divElem.style.visiblity = "hidden";
        }*/
    });
});