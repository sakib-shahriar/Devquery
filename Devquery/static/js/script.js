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

    $("#text-area-comment").keypress(function (e) {
        var key = e.which;
        if(key == 13) {
            var comment = $(this).val()
            if(comment == "") return
            var post_id = $("#post_id").html()
            var action = "make_comment"
            $.ajax({
                type: "GET",
                url: '/ajax',
                data: {
                    action: action,
                    post_id: post_id,
                    comment: comment,
                },
                success: $.proxy(function(data) {
                    $(this).val("")
                    var comment_template  = $(".comment-template").clone()
                    comment_template.css("display", "block")
                    comment_template.find("img").attr("src", data.user_image)
                    comment_template.find("#temp-comment-link").attr("href", data.url)
                    comment_template.find("img").next().html(data.user_name)
                    comment_template.find(".temp-comment").html(data.comment)
                    comment_template.find("#toggle-btn").attr("data-target","#"+data.cmt_id)
                    comment_template.find("#temp-collapse").attr("id",data.cmt_id)
                    comment_template.find(".temp-comment-id").html(data.cmt_id)
                    $(".comment-space").append(comment_template)
                }, this)
            })
        }
    })

    $(function(){
        $('textarea').autoResize({
            'minRows': 2,
            'maxRows': 0
        })

    })


    $( ".nav-search" ).autocomplete({
        source: function( request, response ) {
            var text = $(".nav-search").val()
            $.ajax({
                type: "GET",
                url: '/ajax',
                dataType: "json",
                data: {
                    text: text,
                    action: "search_suggestion",
                },
                success: function (data) {
                    response(data);
                }
            });
        }
    });

    $(".savet").click(function (e) {
        var post_id = $(this).children("p").html()
        var action = "save_post"
        $.ajax({
            type: "GET",
            url: '/ajax',
            data: {
                post_id: post_id,
                action: action,
            },
            success: $.proxy(function(data) {
                if(data.stat == "created"){
                    $(this).children("i").css("color","#2962ff")
                }
                else{
                    $(this).children("i").css("color","#808080")
                }
            }, this)
        });
    })

    $(".temp-class").keypress(function (e) {
        var key = e.which
        if(key == 13){
            var comp = $(e.target)
            if(comp.val()=="") return
            var comment_id = comp.closest(".collapse").attr("id")
            var action = "make_reply"
            $.ajax({
                type: "GET",
                url: '/ajax',
                data: {
                    comment_id: comment_id,
                    reply: comp.val(),
                    action: action,
                },
                success: $.proxy(function(data) {
                    comp.val("")
                    var reply_template = $(".reply-template").clone()
                    reply_template.css("display","block")
                    reply_template.find("#temp-reply-img").attr("src",data.user_image)
                    reply_template.find("#temp-reply-link").attr("href",data.url)
                    reply_template.find("#temp-reply-name").html(data.user_name)
                    reply_template.find("#temp-reply").html(data.rep)
                    comp.parent().parent().parent().parent().next().append(reply_template)
                }, this)
            });
        }
    })
    $(".temp-follow-msg").click(function (e) {
        var comp = $(e.target)
        if(!e.target.matches('button')) return
        if(comp.html() != "Follow" && comp.html() != "Following") return
        var action = "follow"
        var user_id = comp.attr("id")
        $.ajax({
            type: "GET",
            url: '/ajax',
            data: {
                user_id: user_id,
                action: action,
            },
            success: $.proxy(function(data) {
                if(data.stat == 'followed'){
                    comp.html("Following")
                }
                else {
                    comp.html("Follow")
                }
            }, this)
        });
    })

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
    let data = { action: "get_notification_num"};
    let url = "/ajax";
    let requestType = "GET";
    let async = false;
    let callback = (data) => {
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

