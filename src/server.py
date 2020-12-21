import cherrypy
import os

from .model import Base
from .view_app import MainView
from .cherrypy_plugins import SAPlugin, SATool, KeyMgrPlugin, KeyMgrTool


class Server:
    CONFIG = {
        "/static": {
            "tools.staticdir.root": os.path.join(
                os.path.dirname(__file__), "static"),
            "tools.staticdir.on": True,
            "tools.staticdir.dir": ".",
        }
    }

    def __init__(self, virtual_root_path):
        sa_plugin = SAPlugin(cherrypy.engine)
        sa_plugin.to_sqlite("server.db")
        sa_plugin.Base = Base
        sa_plugin.subscribe()

        key_plugin = KeyMgrPlugin(cherrypy.engine, virtual_root_path)
        key_plugin.subscribe()

        cherrypy.tools.dbtool = SATool(sa_plugin)
        cherrypy.tools.keytool = KeyMgrTool(key_plugin)

    def run(self):
        cherrypy.quickstart(MainView(), "/", self.CONFIG)
    
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
