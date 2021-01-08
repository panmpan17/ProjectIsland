// Static files dummy timestamp
var TIMESTAMP = null;
var staticFilesQueue = [
    "/static/theme.css",
    "/static/jspython.js",
    "/static/basic.js",
    "/static/login_stuff.js",
    "/static/popup.js",
];
var head = null;
var body = null;

function AddAutoRenewStaticFiles(url) {
    if (TIMESTAMP == null) {
        if (url instanceof Array) {
            for (var u of url)
                staticFilesQueue.push(u);
        }
        else
            staticFilesQueue.push(u);
    }
    else {
        if (url instanceof Array) {
            for (var u of url)
                AddStaticFilesToHtml(u);
        }
        else
            AddStaticFilesToHtml(u);
    }
}

function AddStaticFilesToHtml(url) {
    if (url.endsWith("css")) {
        var link = document.createElement("link");
        link.rel = "stylesheet";
        link.id = url;
        link.href = url + "?d=" + TIMESTAMP;

        if (head == null) head = document.getElementsByTagName("head")[0];
        head.append(link);
    }
    else {
        var script = document.createElement("script");
        script.src = url + "?d=" + TIMESTAMP;

        if (body == null) body = document.getElementsByTagName("body")[0];
        body.append(script);
    }
}

(function () {
    $.ajax({
        url: window.location.origin + "/timestamp",
        success: function (msg) {
            TIMESTAMP = msg;

            while (staticFilesQueue.length > 0) {
                var url = staticFilesQueue.splice(0, 1)[0];
                AddStaticFilesToHtml(url);

                // staticFilesQueue = ;
            }
        }
    });
})();