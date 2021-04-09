$(document).ready(function () {
    $(window).scroll(function () { 
        if($(window).scrollTop() > 0) {
            $("#navbar").addClass("fixed-top");
         }
        else{
            $("#navbar").removeClass("fixed-top");
        }
    });
});