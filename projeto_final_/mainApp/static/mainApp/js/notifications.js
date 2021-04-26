$(document).ready(function(){


    $(".notification").click(function(){
        var n1 = $(this).attr("id").split("_")[1];
        try{
          var n2 = $(this).attr("id").split("_")[2];
        }
        catch (e) {}

        $(".defaultNotifications").hide();
        $(".contentNotification").hide();
        $("#content_"+n1).show();
        try{
          var id_form = "myform_"+n1+"_"+n2
          $("#"+id_form).submit();
        }catch(e){}
    })
    $('.myform').submit(function(event){
        var n3 = $(this).attr("id").split("_")[1];
        var n4 = $(this).attr("id").split("_")[2];
        event.preventDefault();
        create_post(n3,n4);   
    });
    $('.myformR').submit(function(event){
      var n5 = $(this).attr("id").split("_")[1];
      var n6 = $(this).attr("id").split("_")[2];
      event.preventDefault();
      create_post_refunds(n5,n6);   
    });
    $('.myformTen').submit(function(event){
      var n7 = $(this).attr("id").split("_")[1];
      var n8 = $(this).attr("id").split("_")[2];
      event.preventDefault();
      create_post_tenant(n7,n8);   
    });
    $('.myformInv').submit(function(event){
      var n9 = $(this).attr("id").split("_")[1];
      var n10 = $(this).attr("id").split("_")[2];
      event.preventDefault();
      create_post_invoice(n9,n10);   
    });
    $('.myformWarn').submit(function(event){
      var n11 = $(this).attr("id").split("_")[1];
      var n12 = $(this).attr("id").split("_")[2];
      event.preventDefault();
      create_post_warning(n11,n12);   
    });

})
function create_post(numb,id_req) {
  $.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
  });
  $.ajax({
      url : 'notificationsLandlord/read/'+id_req, // the endpoint
      type : "POST", // http method
      data : {}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#myform_"+numb+"_"+id_req).children().attr('class', 'notification list-group-item list-group-item-action list-group-item-info rounded-0');
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};
function create_post_refunds(numb,id_ref) {
  $.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
  });
  $.ajax({
      url : 'notificationsLandlord/readRef/'+id_ref, // the endpoint
      type : "POST", // http method
      data : {}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#myform_"+numb+"_"+id_ref).children().attr('class', 'notification list-group-item list-group-item-action list-group-item-info rounded-0');
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};
function create_post_tenant(numb,id_req) {
  $.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
  });
  $.ajax({
      url : 'notificationsTenant/read/'+id_req, // the endpoint
      type : "POST", // http method
      data : {}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#myform_"+numb+"_"+id_req).children().attr('class', 'notification list-group-item list-group-item-action list-group-item-info rounded-0');
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};
function create_post_invoice(numb,id_inv) {
  $.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
  });
  $.ajax({
      url : 'notificationsLandlord/readInv/'+id_inv, // the endpoint
      type : "POST", // http method
      data : {}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#myform_"+numb+"_"+id_inv).children().attr('class', 'notification list-group-item list-group-item-action list-group-item-info rounded-0');
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};
function create_post_warning(numb,id_warn) {
  $.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
  });
  $.ajax({
      url : 'notificationsLandlord/readWarn/'+id_warn, // the endpoint
      type : "POST", // http method
      data : {}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#myform_"+numb+"_"+id_warn).children().attr('class', 'notification list-group-item list-group-item-action list-group-item-info rounded-0');
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};