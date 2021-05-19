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
    update_num_of_unread_messages();
});

var myinterval;
function update_num_of_unread_messages(){
    clearInterval(myinterval);
    console.log("entrou")
    myinterval = setInterval(
        function(){
            $.ajax({
                url : "/mainApp/numOfunreadedMessages/",
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