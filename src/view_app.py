import cherrypy


class View:
    def render_html(self, html_file):
        pass


class MainView(View):
    @cherrypy.expose
    def index(self):
        return "Hellow World!"
