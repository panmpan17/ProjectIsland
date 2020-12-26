BASIC_JS_LOADED = true;

// Form Handling
function GetFormFieldsData(formEle) {
    var data = {};

    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" || tagName == "TEXTAREA") {
            var field = ele.attributes.getNamedItem("field");

            if (field != null) {
                if (ele.value == "")
                    return null;

                data[field.value] = ele.value;
            }
        }
    }

    return data;
}

function FillFormFieldswithData(formEle, data) {
    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" || tagName == "TEXTAREA") {
            var field = ele.attributes.getNamedItem("field");

            if (field != null) {
                if (data[field.value] != undefined)
                    ele.value = data[field.value];
            }
        }
    }
}

function ClearFormField(formEle) {
    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT" || tagName == "TEXTAREA") {
            ele.value = "";
        }
    }
}


// Restful API
function Get(url, data, success, error) {
    var key = GetCookie("key");
    if (key != "")
        data.key = key;

    $.ajax({
        url: location.origin + url,
        data,
        success,
        error,
    });
}

function Post(url, data, success, error) {
    var key = GetCookie("key");
    if (key != "")
        data.key = key;

    $.ajax({
        url: location.origin + url,// "/rest/website_news_sub/",
        type: "POST",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        success,
        error,
    });
}


// Cookies
function StoreCookie(name, value, expires = "", path = "/") {
    if (expires == "") expires = "Session";
    else {
        var today = new Date();
        today.setDate(today.getDate() + expires);
        expires = today.toUTCString();
    }

    document.cookie = `${name}=${value}; expires=${expires}; path=${path}`;
}

function GetCookie(name) {
    name += "=";

    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }

    return "";
}

function DeleteCookie(name, path = "/") {
    document.cookie = `${name}=; expires= Thu, 01 Jan 1970 00:00:00 GMT; path=${path}`;
}

// Date
function ParseDatetime(data) {
    var now = new Date();
    return new Date(data * 1000 - (now.getTimezoneOffset() * 60 * 1000))
}

function GetUrlParams() {
    var paramsString = location.search.replace("?", "").split("&");
    var params = {};

    for (var paramString of paramsString) {
        var index = paramString.indexOf("=");
        params[paramString.substring(0, index)] = decodeURIComponent(paramString.substring(index + 1));
    }

    return params;
}

(function () {
    document.dispatchEvent(new CustomEvent("basic_js_loaded"));
})();