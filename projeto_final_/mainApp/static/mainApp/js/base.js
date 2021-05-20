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

    update_num_of_unread_notifications()

    update_num_of_unread_messages();
});

var myinterval_notifications;
function update_num_of_unread_notifications(){
    clearInterval(myinterval_notifications);
    myinterval_notifications = setInterval(
        function(){
            $.ajax({
                url : "/mainApp/num_of_unread_notifications",
                type : "GET",
                data : {}, 

                success : function(json) {
                    let data = JSON.parse(json);
                    $("#numUnreadNotifications").text(data["numUnreadNotifications"]);
                }
            });
        }, 2000
    )

} 


var myinterval;
function update_num_of_unread_messages(){
    clearInterval(myinterval);
    myinterval = setInterval(
        function(){
            $.ajax({
                url : "/mainApp/numOfunreadMessages/",
                type : "GET",
                data : {}, 
        
                success : function(json) {
                    let data = JSON.parse(json);
                    $("#unreadedMessages").text(data["numUnreadMessages"]);
                }
            });
        }, 4000
    )

}
