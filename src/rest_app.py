import cherrypy


class View:
    pass


class RestMainView(View):
    def __init__(self):
        self.website_news_sub = WebsiteNewsSubscriptionView()


class WebsiteNewsSubscriptionView(View):
    @cherrypy.expose
    def index(self):
        return "a"
