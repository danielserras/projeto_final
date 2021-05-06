$(document).ready(function () {
    $("#sendMessageRow").hide();
    $(".selectChat").submit(function (e) { 
        e.preventDefault();
        select_chat(this);
        $("#sendMessageRow").show();
    });

    $("#sendMessage").submit(function (e) { 
        e.preventDefault();
        send_message(this);
    });
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": csrf_token }
        });
    });
});
var myinterval;
function select_chat(form){
    clearInterval(myinterval);
    var pathname = window.location.pathname;
    var chat = form.childNodes[3].value;

    $(".chat-select").each(function (index, element) {
        $(this).removeClass("bg-info")
        $($(this).children()[0]).removeClass("text-white").addClass("text-info");
    });
    var select_id = "#chat_div_" + chat;
    $(select_id).removeClass();
    $(select_id).addClass("row px-2 py-3 border-bottom border-info chat-select bg-info");
    $($(select_id).children()[0]).removeClass("text-info").addClass("text-white");


    $.ajax({
        url : pathname,
        type : "GET",
        data : { chat_id : chat }, 

        success : function(json) {
            show_messages(json, chat)
        }
    });
    myinterval = setInterval(
        function(){
            $.ajax({
                url : pathname,
                type : "GET",
                data : { chat_id : chat }, 
        
                success : function(json) {
                    show_messages(json, chat)
                }
            });
        }, 4000
    )
}
function send_message(form){
    var pathname = window.location.pathname;
    var chat = $("#chat").val();
    var content = $("#message").val();
    $("#message").val("");
    $.ajax({
        url : pathname, 
        type : "POST", 
        data : { "chat_id":chat, "content":content}, 

        success : function(json) {
            show_messages(json, chat);
        }
    });
}

function show_messages(json, chat_id){
    let response = JSON.parse(json);
    let messages_box = $("#messagesBox"); 
    messages_box.html("");
    let username = response["username"];
    $("#receiver").html("");
    $("#receiver").append(response["receiver"]);
    $("#chat").val(chat_id);
    for(const [key, value] of Object.entries(response["messages"])){
        if(value["sender"] == username){
            messages_box.append('<div class="col-sm-6 shadow-lg ml-auto mt-3 p-3 rounded border border-primary msg"><p>'+value["content"]+'</p><p class="m-0 p-0 font-weight-light text-muted">'+value["timestamp"]+'</p></div>');
        }
        else{
            messages_box.append('<div class="col-sm-6 shadow-lg mb-3 p-3 mt-3 rounded border border-secondary msg"><p>'+value["content"]+'</p><p class="m-0 p-0 font-weight-light text-muted">'+value["timestamp"]+'</p></div>');
        }
    }

    if($(".msg")[0]){
        console.log("SIM")
        $("#messagesBox").animate({ scrollTop: $('#messagesBox').prop("scrollHeight")}, 1000);
    }
}