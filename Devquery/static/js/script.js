$( document ).ready(function() {
    $("#form-register").on('submit', (e) => {
        const data = {
            username: $("#username-register").val(),
            email: $("#email-register").val(),
            action: "registration_validation",
        };
        const url = "/ajax";
        const requestType = "GET";
        const async = false;
        const callback = (data) => {
            const message = $(".msg");
            if (data.stat != "success") {
                e.preventDefault();
                message.html(data.stat);
                message.css("display", "block");
            }
            else {
                const tags = $('[name="tags[]"]:checked');
                if (tags.length < 2) {
                    e.preventDefault();
                    message.html("You have to select at least 2 tags");
                    message.css("display", "block")
                }
            }
        };
        sendRequest(data, url, requestType, async, callback);
    });

    $(".status-btn").on('click', (e) => {
        const _el = $(e.currentTarget);
        if (!_el.hasClass('plus') && !_el.hasClass('minus')) return;
        const data = {
            action: _el.hasClass('plus') ? "plus_vote" : "minus_vote",
            post_id: _el.closest('.row').attr('id')
        };
        const url = "/ajax";
        const requestType = "GET";
        const async = false;
        const callback = (data) => {
            let label = _el.find(".vote-count");
            if (data.stat == "created") {
                $(_el).css('color','#2962ff');
                let vote = parseInt(label.html());
                label.html(vote + 1);
            }
            else if (data.stat == "deleted") {
                _el.css('color','black');
                let vote = parseInt(label.html());
                label.html(vote - 1)
            }
            else {
                if (_el.hasClass('plus')) {
                    label = _el.parent().next().find(".vote-count");
                    let vote = parseInt(label.html());
                    label.html(vote - 1);
                    _el.parent().next().find(".minus").css('color','black');
                }
                else {
                    label = _el.parent().prev().find(".vote-count");
                    let vote = parseInt(label.html());
                    label.html(vote - 1);
                    _el.parent().prev().find(".plus").css('color','black');
                }
                label = _el.find(".vote-count");
                let vote = parseInt(label.html());
                _el.css('color','#2962ff');
                label.html(vote + 1);
            }
        };
        sendRequest(data, url, requestType, async, callback);
    });

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

    $(".save-post").on('click', (e) => {
        const _el =  $(e.currentTarget);
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

    $(".drop-clk").on('click', () => {
        const data = {};
        const url = "/getPopupNotification";
        const requestType = "GET";
        const async = false;
        const callback = (data) => $(".pop-not-list").empty().append(data);
        sendRequest(data, url, requestType, async, callback);
    });

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
});

setInterval(updateNotification, 10000);

const updateNotification = () => {
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
};

