import cherrypy

from .model import Base
from .view_app import MainView
from .cherrypy_plugins import SAPlugin, SATool


class Server:
    def __init__(self):
        sa_plugin = SAPlugin(cherrypy.engine)
        sa_plugin.to_sqlite("server.db")
        sa_plugin.Base = Base
        sa_plugin.subscribe()

        cherrypy.tools.dbtool = SATool(sa_plugin)

    def run(self):
        cherrypy.quickstart(MainView())
    
    def wsgi_application(self):
        import sys

        sys.stdout = sys.stderr

        cherrypy.config.update({"enviroment": "embedded"})

        if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
            import atexit

            cherrypy.engine.start(blocking=False)
            atexit.register(cherrypy.engine.stop)
        
        application = cherrypy.Application(
            MainView(), script_name='', config=None)

        return application
