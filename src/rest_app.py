import cherrypy


class View:
    _cp_config = {
        "tools.json_out.on": True,
        "tools.json_in.on": True,
        "tools.dbtool.on": True,
        "tools.encode.on": True,
    }


class RestMainView(View):
    def __init__(self):
        self.website_news_sub = WebsiteNewsSubscriptionView()


class WebsiteNewsSubscriptionView(View):
    @cherrypy.expose
    def index(self):
        with cherrypy.request.db.session_scope() as session:
            print(session)

        return "a"
