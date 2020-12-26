import cherrypy
import jinja2
import os.path

from .rest_app import RestMainView
from datetime import datetime


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), "templates")))


TIMESTAMP = str(int(datetime.now().timestamp()))


class View:
    @staticmethod
    def render_html(html_file, **params):
        t = jinja_env.get_template(html_file)
        return t.render(params)


class MainView(View):
    def __init__(self):
        self.rest = RestMainView()

    @cherrypy.expose
    def index(self, **kwargs):
        return self.render_html("index.html")
    
    @cherrypy.expose
    def login(self, **kwargs):
        return self.render_html("login.html")
    
    @cherrypy.expose
    def forum(self, *args, **kwargs):
        return self.render_html("forum.html")

    @cherrypy.expose
    def timestamp(self, **kwargs):
        return TIMESTAMP
