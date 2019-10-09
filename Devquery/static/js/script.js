$( document ).ready(function() {
    $("#form-register").submit(function (e) {
        var action = "registration_validation"
        var username = $("#username-register").val()
        var email = $("#email-register").val()
        $.ajax({
            type: "GET",
            async: false,
            url: '/ajax',
            data: {
                username: username,
                email: email,
                action: action,
            },
            success: $.proxy(function(data) {
                if(data.stat != "success"){
                    e.preventDefault()
                    $(".msg").html(data.stat)
                    $(".msg").css("display", "block")
                }
                else{
                    var tags = $('[name="tags[]"]:checked')
                    if(tags.length < 2){
                        e.preventDefault()
                        $(".msg").html("You have to select at least 2 tags")
                        $(".msg").css("display", "block")
                    }
                }
            }, this)
        });
    })


    $(".status-btn").click(function (e) {
        var action
        if($(this).attr('id') == "plus") action = "plus_vote"
        else if($(this).attr('id') == "minus") action = "minus_vote"
        else return
        var post_id = $(this).parent().parent().children("p").html()
        $.ajax({
            type: "GET",
            url: '/ajax',
            data: {
                action:action,
                post_id:post_id,
            },
            success: $.proxy(function(data) {
                if(data.stat == "created"){
                    $(this).css('color','#2962ff')
                    var vote = parseInt($(this).children("span").html())
                    $(this).children("span").html(vote + 1)
                }
                else if(data.stat == "deleted"){
                    $(this).css('color','black')
                    var vote = parseInt($(this).children("span").html())
                    $(this).children("span").html(vote - 1)
                }
                else{
                    if($(this).attr('id') == "plus") {
                        var vote = parseInt($(this).parent().next().children("button").children("span").html())
                        $(this).parent().next().children("button").children("span").html(vote - 1)
                        $(this).parent().next().children("button").css('color','black')
                    }
                    else {

                        var vote = parseInt($(this).parent().prev().children("button").children("span").html())
                        $(this).parent().prev().children("button").children("span").html(vote - 1)
                        $(this).parent().prev().children("button").css('color','black')
                    }
                    vote = parseInt($(this).children("span").html())
                    $(this).css('color','#2962ff')
                    $(this).children("span").html(vote + 1)
                }
            }, this)
        })
    })


    $(".temp-class").click(function (e) {
        var comp = $(e.target)
        if(e.target.matches('i') || e.target.matches('span')){
            comp = $(e.target).parent()
        }
        var action
        if(comp.attr('id') == "plus") action = "comment_plus_vote"
        else if(comp.attr('id') == "minus") action = "comment_minus_vote"
        else return
        var comment_id = comp.parent().parent().children("p").html()
        $.ajax({
            type: "GET",
            url: '/ajax',
            data: {
                action:action,
                comment_id:comment_id,
            },
            success: $.proxy(function(data) {
                if(data.stat == "created"){
                    comp.css('color','#2962ff')
                    var vote = parseInt(comp.children("span").html())
                    comp.children("span").html(vote + 1)
                }
                else if(data.stat == "deleted"){
                    comp.css('color','black')
                    var vote = parseInt(comp.children("span").html())
                    comp.children("span").html(vote - 1)
                }
                else{
                    if(comp.attr('id') == "plus") {
                        var vote = parseInt(comp.parent().next().children("button").children("span").html())
                        comp.parent().next().children("button").children("span").html(vote - 1)
                        comp.parent().next().children("button").css('color','black')
                    }
                    else {
                        var vote = parseInt(comp.parent().prev().children("button").children("span").html())
                        comp.parent().prev().children("button").children("span").html(vote - 1)
                        comp.parent().prev().children("button").css('color','black')
                    }
                    vote = parseInt(comp.children("span").html())
                    vote = parseInt(comp.children("span").html())
                    comp.css('color','#2962ff')
                    comp.children("span").html(vote + 1)
                }
            }, this)
        })
    })

    $("#text-area-comment").on('keypress', (e) => {
        const _el = $("#text-area-comment");
        const key = e.which;
        if (key == 13) {
            const comment = $(_el).val();
            if (comment == "") return;
            _el.val("");
            const data = {
                post_id: $("#post_id").html(),
                comment: comment
            };
            const url = '/post/getComment';
            const requestType = "GET";
            const async = false;
            const callback = (data) => $(".comment-space").append(data);
            sendRequest(data, url, requestType, async, callback);
        }
    });

    $(() => {
        $('textarea').autoResize({
            'minRows': 2,
            'maxRows': 0
        })

    });

    $( ".nav-search" ).autocomplete({
        source: (request, response) => {
            const data = {
                text: $(".nav-search").val(),
                action: "search_suggestion",
            };
            const url = '/ajax';
            const requestType = "GET";
            const async = false;
            const callback = (data) => response(data);
            sendRequest(data, url, requestType, async, callback);
        }
    });

    $(".savet").on('click', () => {
        const _el =  $(".savet");
        const data = {
            post_id: _el.children("p").html(),
            action: "save_post"
        };
        const url = '/ajax';
        const requestType = "GET";
        const async = false;
        const callback = (data) => {
            data.stat == "created" ? $(_el).children("i").css("color","#2962ff") :  $(_el).children("i").css("color","#808080");
        };
        sendRequest(data, url, requestType, async, callback);
    });

    $(".temp-class").on('keypress', (e) => {
        const _el = $(".temp-class");
        const key = e.which;
        if (key == 13) {
            const comp = $(e.target);
            const reply = comp.val();
            if (reply == "") return;
            comp.val("");
            const data = {
                comment_id: comp.closest(".collapse").attr("id"),
                reply: reply,
            };
            const url = '/post/getReply';
            const requestType = "GET";
            const async = false;
            const container = comp.parent().parent().parent().parent().next();
            const callback = (data) => container.append(data);
            sendRequest(data, url, requestType, async, callback);
        }
    });

    $(".temp-follow-msg").on('click', (e) => {
        const _el = $(".temp-follow-msg");
        const comp = $(e.target)
        if (!e.target.matches('button')) return;
        if (comp.html() != "Follow" && comp.html() != "Following") return;
        const data = {
            user_id: comp.attr("id"),
            action: "follow"
        };
        const url = '/ajax';
        const requestType = "GET";
        const async = false;
        const callback = (data) => {
            data.stat == 'followed' ? comp.html("Following") : comp.html("Follow");
        };
        sendRequest(data, url, requestType, async, callback);
    });

    $(".drop-clk").click(function (e) {
        var action = "get_notifications"
        $.ajax({
            type: "GET",
            url: '/ajax',
            data: {
                action: action,
            },
            success: $.proxy(function(data) {
                $(".pop-not-list").empty()
                if(data.length > 0){
                    data.forEach(function (notf) {
                        var notification = $("#not-template").clone()
                        notification.find("#notf-detail").html(notf.notification)
                        notification.find("#notf-time").html(notf.time)
                        notification.find("#notf-id").html(notf.id)
                        notification.find("#notf-image").attr("src", notf.image)
                        notification.find("#notf-link").attr("href", notf.url)
                        notification.css("display", "block")
                        console.log(notf)
                        if(notf.is_read == '0'){
                            notification.find("#notf-link").addClass("not-read")
                        }
                        else {
                            notification.find("#notf-link").removeClass("not-read")
                        }
                        $(".pop-not-list").append(notification)
                    })
                    var notf_btns = $("#not-btn").clone()
                    notf_btns.css("display", "block")
                    $(".pop-not-list").append(notf_btns)
                }
                else{
                    var notification = $("#not-template-empty").clone()
                    notification.css("display", "block")
                    $(".pop-not-list").append(notification)
                }

            }, this)
        });
    })

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
})

var myVar = setInterval(updateNotification, 10000);

function updateNotification() {
    const data = { action: "get_notification_num"};
    const url = "/ajax";
    const requestType = "GET";
    const async = false;
    const callback = (data) => {
        if(data.num == "none") return;
        let _el = $("#notification-badge");
            if(data.num > 9) {
                _el.html("9+");
                _el.css("display", "block");
            }
            else if(data.num == 0) {
                _el.html("0");
                _el.css("display", "none");

            }
            else{
                _el.html(data.num);
                _el.css("display", "block");
            }
    };
    sendRequest(data, url, requestType, async, callback);
}

