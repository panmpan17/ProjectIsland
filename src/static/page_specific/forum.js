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

function SubmitNewReply(formEle) {
    var data = GetFormFieldsData(formEle);

    if (data == null) {
        alert("請填寫完整");
        return;
    }
    else {
        Post("/rest/forum/reply", data, function (msg) {
            viewmodel.openedPost().FetchAllComment();
            ClearFormField(formEle);
        }, function (err) {
            console.log(err)
        });
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

    this.comments = ko.observableArray([]);
    
    this.hasComments = ko.computed(function () {
        return self.comments().length > 0;
    }, this);

    this.commentsLength = ko.computed(function () {
        return self.comments().length;
    }, this);

    this.visibleComments = ko.computed(function () {
        return self.comments();
    }, this);

    this.OpenPost = function () {
        viewmodel.ShowPost(self);
    }

    this.FetchAllComment = function () {
        Get("/rest/forum/reply", {post_id: self.id}, function (msg) {
            // console.log(msg);
            self.comments.removeAll();

            for (row of msg.data) {
                self.comments.push(new ForumReply(row));
            }

            self.comments.sort(function (a, b) {
                return a.create_at - b.create_at;
            });
        }, function () { });
    }
}

var ForumReply = function (data) {
    var self = this;

    this.id = data.id;
    this.content = data.content;
    this.author = data.author;
    this.create_at = ParseDatetime(data.create_at);
    this.formatedCreateAt = this.create_at.strftime("%Y/%m/%d %H:%M:%S");
    // console.log(this.author);
}

function AppViewModel() {
    var self = this;

    this.posts = ko.observableArray([]);
    this.openedPost = ko.observable();

    this.visiblePosts = ko.computed(function () {
        return self.posts();
    }, this);


    this.FetchAllForumPost = function () {
        Get("/rest/forum/post", {}, function (msg) {
            self.posts.removeAll();

            for (row of msg.data) {
                var forumPost = new ForumPost(row);
                forumPost.FetchAllComment();
                self.posts.push(forumPost);
            }

            self.posts.sort(function (a, b) {
                return b.create_at - a.create_at;
            });
        }, function () { });
    }

    this.ShowPost = function (post) {
        OpenPopup("post-detail");
        self.openedPost(post);
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