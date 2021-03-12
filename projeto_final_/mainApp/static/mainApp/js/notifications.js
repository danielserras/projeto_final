$(document).ready(function(){

    

    //$(".notification").click(function(){
      //  $(".defaultNotifications").hide();
      //  $(".contentNotification").show();
    
    //})

    $(".notification").click(function(){
        var n1 = $(this).attr("id").split("_")[1];
        $(".defaultNotifications").hide();
        $(".contentNotification").hide();
        $("#content_"+n1).show();
        
        
    
    })

})