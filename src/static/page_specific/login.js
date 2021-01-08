var RedirectPath = "/";

function SubmitSignup(formEle) {
    var data = GetFormFieldsData(formEle);

    if (data == null) {
        alert("請填寫完整");
        return;
    }
    else {
        data.password = sha256(data.password);

        Post("/rest/account/signup", data, function (msg) {
            StoreCookie("key", msg.key);
            location = RedirectPath;
        }, function (err) {
            if (err.responseJSON.reason == "Repeated login_id") {
                alert("帳號重複");
            }
        });
    }
}

function SubmitLogin(formEle) {
    var data = GetFormFieldsData(formEle);

    if (data == null) {
        alert("請填寫完整");
        return;
    }
    else {
        data.password = sha256(data.password);

        Post("/rest/account/login", data, function (msg) {
            StoreCookie("key", msg.key);
            location = RedirectPath;
        }, function (err) {
            if (err.responseJSON.reason == "Field wrong") {
                alert("帳號密碼錯誤");
            }
            else if (err.responseJSON.reason == "Human failed") {
                alert("人類認證失敗");
            }
        });
    }
}

(function () {
    var params = GetUrlParams();
    if (params.back != undefined) {
        RedirectPath = params.back;
    }

    if (GetCookie("key") != "") {
        location = RedirectPath;
        return;
    }

    // var user = {
    //     login_id: "panmichael",
    //     password: "panpan",
    //     email: "panmpan@gmail.com",
    //     nickname: "Michael",
    // };
    // FillFormFieldswithData(document.getElementById("signup"), user);
    // FillFormFieldswithData(document.getElementById("login"), user);
})();