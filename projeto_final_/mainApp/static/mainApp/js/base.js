$(document).ready(function () {
    $(window).scroll(function () { 
        if($(this).scrollTop() > 0) {
            $("#navbar").addClass("fixed-top");
         }
        else{
            $("#navbar").removeClass("fixed-top");
        }

        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });
    
    $('#back-to-top').click(function () {
        $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    
    $('#back-to-top').tooltip('show');
});
