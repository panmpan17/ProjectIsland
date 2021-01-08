var LoginStatusListener = [];
var accountInfo = null;


function GoToLoginPage() {
    if (location.pathname == "/login")
        return;

    location = "/login?back=" + encodeURI(location.pathname);
}

function TurnOnLoginElements(showLoginedElement, showUnloginedElement) {
    for (var i = 0; i < document.styleSheets.length; i++) {
        var styleSheet = document.styleSheets[i];
        if (styleSheet.href == null) {
            var loginCssChanges = false;
            var unloginCssChanges = false;
            for (var e = 0; e < styleSheet.cssRules.length; e++) {
                var rule = styleSheet.cssRules[e];
                if (rule.selectorText == "[name=\"logined-element\"]") {
                    rule.style.display = showLoginedElement? "block": "none";
                    loginCssChanges = true;
                }
                if (rule.selectorText == "[name=\"unlogined-element\"]") {
                    rule.style.display = showUnloginedElement ? "block" : "none";
                    unloginCssChanges = true;
                }

                if (loginCssChanges && unloginCssChanges)
                    return;
            }
        }
    }
}


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
        // var loginedElements = document.getElementsByName("unlogined-element");
        // for (var ele of loginedElements) {
        //     ele.style.display = "block";
        // }

        TurnOnLoginElements(false, true);
    }
    else {
        $.ajax({
            url: location.origin + "/rest/account/me",
            data: { key: keyCookie },
            success: function (msg) {
                accountInfo = msg;
                delete accountInfo.success;

                // var loginedElements = document.getElementsByName("logined-element");
                // for (var ele of loginedElements) {
                //     ele.style.display = "block";
                // }

                TurnOnLoginElements(true, false);
            },
            error: function (error) {
                document.cookie = "key=; expires= Thu, 01 Jan 1970 00:00:00 GMT";

                // var loginedElements = document.getElementsByName("unlogined-element");
                // for (var ele of loginedElements) {
                //     ele.style.display = "block";
                // }

                TurnOnLoginElements(false, true);
            }
        });
    }
})();

function Logout() {
    DeleteCookie("key");
    location.reload();
}