function SubmitNewPost(formEle) {
    var data = GetFormFieldsData(formEle);

    if (data == null) {
        alert("請填寫完整");
        return;
    }
    else {
        Post("/rest/forum/post", data, function (msg) {
            viewmodel.FetchAllForumPost();
            ClearFormField(formEle);
        }, function (err) {
            console.log(err);
        })
    }
}

var ForumPost = function (data) {
    var self = this;

    this.id = data.id;
    this.title = data.title;
    this.content = data.content.replace(/\n/g, "<br>");
    this.cover_img = data.cover_img;
    this.topic = data.topic;
    this.author = data.author;
    this.views_count = data.views_count;
    this.create_at = ParseDatetime(data.create_at);
    this.formatedCreateAt = this.create_at.strftime("%Y/%m/%d %H:%M:%S");
}

function AppViewModel() {
    var self = this;

    this.posts = ko.observableArray([]);

    this.visiblePosts = ko.computed(function () {
        return self.posts();
    }, this);


    this.FetchAllForumPost = function () {
        Get("/rest/forum/post", {}, function (msg) {
            self.posts.removeAll();

            for (row of msg.data) {
                self.posts.push(new ForumPost(row));
            }
        }, function () { });
    }
}

var viewmodel;
function main() {
    viewmodel = new AppViewModel();
    ko.applyBindings(viewmodel);
    viewmodel.FetchAllForumPost();
}

if (window.BASIC_JS_LOADED) main();
else document.addEventListener("basic_js_loaded", main);