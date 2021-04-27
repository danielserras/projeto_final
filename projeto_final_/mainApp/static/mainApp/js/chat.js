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

function select_chat(form){
    var pathname = window.location.pathname;
    var chat = form.childNodes[3].value;

    $.ajax({
        url : pathname,
        type : "GET",
        data : { chat_id : chat }, 

        success : function(json) {
            show_messages(json, chat)
        }
    });
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
            show_messages(json, chat)
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
            messages_box.append('<div class="col-sm-6 shadow-lg ml-auto mt-3 p-3 border border-primary"><p>'+value["content"]+'</p><p class="m-0 p-0 font-weight-light text-muted">'+value["timestamp"]+'</p></div>');
        }
        else{
            messages_box.append('<div class="col-sm-6 shadow-lg mb-3 p-3 rounded border border-secondary"><p>'+value["content"]+'</p><p class="m-0 p-0 font-weight-light text-muted">'+value["timestamp"]+'</p></div>');
        }
    }
}