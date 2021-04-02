$(document).ready(function () {
    $(".isActive").change(function (e) { 
        e.preventDefault();
        $(this).parent()[0].submit();
    });
});