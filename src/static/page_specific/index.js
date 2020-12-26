function AddSubscription() {
    var email = document.getElementById("email").value;

    if (email == "")
        return;

    Post("/rest/website_news_sub/", { email }, function (msg) {
        document.getElementById("email").value = "";
        viewmodel.FetchAllWebsiteNewsSubscription();
    });
}

function DeleteAllSubscription() {
    $.ajax({
        url: location.origin + "/rest/website_news_sub/",
        type: "DELETE",
        success: function (msg) {
            viewmodel.FetchAllWebsiteNewsSubscription();
        }
    });
}

var WebsiteNewsSubscription = function (data) {
    var self = this;

    this.id = ko.observable(data.id);
    this.email = ko.observable(data.email);
    this.type = ko.observable(data.type);
    this.ip = ko.observable(data.ip);
    this.create_at = ko.observable(data.create_at);

    this.formated = function () {
        return `${self.id()}<br>${self.email()}<br>${self.type()}<br>${self.ip()}<br>${self.create_at()}`;
    }
}

function AppViewModel() {
    var self = this;

    this.subscriptions = ko.observableArray([]);

    this.visibleSubscriptions = ko.computed(function () {
        return self.subscriptions().filter(function (location) {
            return location;
        });
    }, this);

    this.FetchAllWebsiteNewsSubscription = function () {
        $.ajax({
            url: location.origin + "/rest/website_news_sub/",
            success: function (msg) {
                self.subscriptions.removeAll();

                for (row of msg.data) {
                    self.subscriptions.push(new WebsiteNewsSubscription(row));
                }
            }
        });
    }

    this.Logout = function () {
        DeleteCookie("key");
    }
}

var viewmodel;
function main() {
    viewmodel = new AppViewModel();
    ko.applyBindings(viewmodel);
    viewmodel.FetchAllWebsiteNewsSubscription();
}

if (window.BASIC_JS_LOADED) main();
else document.addEventListener("basic_js_loaded", main);