var LoginStatusListener = [];
var accountInfo = null;


(function () {

    var keyCookie = "";
    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf("key=") == 0) {
            keyCookie = c.substring("key=".length, c.length);
            break;
        }
    }

    if (keyCookie == "") {
        var loginedElements = document.getElementsByName("unlogined-element");
        for (var ele of loginedElements) {
            ele.style.display = "block";
        }
    }
    else {
        $.ajax({
            url: location.origin + "/rest/account/me",
            data: { key: keyCookie },
            success: function (msg) {
                accountInfo = msg;
                delete accountInfo.success;

                var loginedElements = document.getElementsByName("logined-element");
                for (var ele of loginedElements) {
                    ele.style.display = "block";
                }
            },
            error: function (error) {
                document.cookie = "key=; expires= Thu, 01 Jan 1970 00:00:00 GMT";

                var loginedElements = document.getElementsByName("unlogined-element");
                for (var ele of loginedElements) {
                    ele.style.display = "block";
                }
            }
        });
    }
})();

function Logout() {
    DeleteCookie("key");
    location.reload();
}