
$(document).ready(function(){
    var previous_page = document.referrer;

    if (previous_page.includes('/accounts/password_reset/')){
        $('#mail_popup').modal('show');
        $('#close_mail_popup').click(function(){
            $('#mail_popup').modal('hide');
        })
        $('.close').click(function(){
            $('#mail_popup').modal('hide');
        })
    }

    if (previous_page.includes('/accounts/reset/MQ/set-password/')){
        $('#reset_done').modal('show');
        $('#close_reset_done').click(function(){
            $('#reset_done').modal('hide');
        })
        $('.close').click(function(){
            $('#reset_done').modal('hide');
        })
    }
})
