let sendRequest = (data, url, requestType, async, callback) => {
    $.ajax({
            type: requestType,
            async: async,
            url: url,
            data: data,
            success: $.proxy(callback, this)
        });
};