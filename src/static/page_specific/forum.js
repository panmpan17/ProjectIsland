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
    this.content = data.content;
    this.cover_img = data.cover_img;
    this.topic = data.topic;
    this.views_count = data.views_count;
    this.create_at = ParseDatetime(data.create_at);

    this.formated = function () {
        return `<h3>${self.title}</h3>${self.content}<br>${self.create_at.strftime("%Y/%m/%d %H:%M:%S")}`;
    }
}

function AppViewModel() {
    var self = this;

    this.posts = ko.observableArray([]);
    this.isLogined = ko.observable(GetCookie("key") != "");

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

var viewmodel = new AppViewModel();
ko.applyBindings(viewmodel);
viewmodel.FetchAllForumPost();