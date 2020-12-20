function GetFormFieldsData(formEle) {
    var data = {};

    for (var i = 0; i < formEle.children.length; i++) {
        var ele = formEle.children[i];
        var tagName = ele.tagName;

        if (tagName == "INPUT") {
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

        if (tagName == "INPUT") {
            var field = ele.attributes.getNamedItem("field");

            if (field != null) {
                if (data[field.value] != undefined)
                    ele.value = data[field.value];
            }
        }
    }
}

function Post(url, data, success, error) {
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