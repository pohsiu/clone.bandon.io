function postMessage() {
    var inputMsg = $("#btn-input").val();
    
    if(inputMsg!=""){
    userMsg(inputMsg);
    
    $.post(
            "/frontend/post_msg",
            {inputMsg:inputMsg},
            function(response) {
                robotMsg(response);
            }
        );
    }
    
    

    
    
    
}

function robotMsg(feedback){
    $("#chatbox").append('\
    <li class="left clearfix">\
        <span class="chat-img pull-left">\
        <img src="http://placehold.it/50/55C1E7/fff&amp;text=!" alt="User Avatar" class="img-circle">\
        </span>\
        <div class="chat-body clearfix">\
            <div class="header">\
                <strong class="primary-font">小幫手</strong>\
            </div>\
            <p>'+feedback+'\
            </p>\
        </div>\
    </li>\
    ');
    scrolling();
    }
function userMsg(msg){
    $("#chatbox").append('\
    <li class="right clearfix">\
        <span class="chat-img pull-right">\
        <img src="http://placehold.it/50/FA6F57/fff&amp;text=ME" alt="User Avatar" class="img-circle">\
        </span>\
        <div class="chat-body clearfix">\
            <div class="header">\
                <span>&nbsp</span>\
                <strong class="pull-right primary-font">'+member_name+'</strong>\
            </div>\
            <p class="pull-right">'+msg+'\
            </p>\
        </div>\
    </li>\
    ');
    $("#btn-input").val("");
    scrolling();
}
function scrolling(){
    var chatdiv = document.getElementById("panel-body");
    chatdiv.scrollTop = chatdiv.scrollHeight;
}