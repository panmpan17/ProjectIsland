var backdropTemplate;
var backdropActivedList = [];

function BackdropCallback(backdropEle) {
    for (var i = 0; i < backdropActivedList.length; i++) {
        if (backdropActivedList[i].backdrop == backdropEle) {
            var data = backdropActivedList.pop(i);

            window.body.removeChild(data.backdrop);
            data.popup.style.display = "none";
            return;
        }
    }
}

function CloseCurrentPopup() {
    if (backdropActivedList.length > 0) {
        var data = backdropActivedList.pop();

        window.body.removeChild(data.backdrop);
        data.popup.style.display = "none";
    }
}

function OpenPopup(popup) {
    if (typeof popup == "string") {
        popup = document.getElementById(popup);
    }

    if (popup.style.display == "block")
        return;

    var cloneBackdrop = backdropTemplate.cloneNode();

    if (window.body == undefined)
        window.body = document.getElementsByTagName("body")[0];

    window.body.appendChild(cloneBackdrop);

    var zIndex = backdropActivedList.length + 1;

    cloneBackdrop.style.display = "block";
    cloneBackdrop.style.zIndex = zIndex - 1;
    popup.style.display = "block";
    popup.style.zIndex = zIndex;

    backdropActivedList.push({
        backdrop: cloneBackdrop,
        popup
    });
}

(function () {
    backdropTemplate = document.getElementById("backdrop-template");
})();