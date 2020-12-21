import cherrypy
import os
import sys

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

    @staticmethod
    def test_wsgi_application(application):
        cherrypy.tree.graft(application, '/')

    def __init__(self, virtual_root_path):
        self.sa_plugin = SAPlugin(cherrypy.engine)
        self.sa_plugin.to_sqlite("server.db")
        self.sa_plugin.Base = Base
        self.sa_plugin.subscribe()

        self.key_plugin = KeyMgrPlugin(cherrypy.engine, virtual_root_path)
        self.key_plugin.subscribe()

        cherrypy.tools.dbtool = SATool(self.sa_plugin)
        cherrypy.tools.keytool = KeyMgrTool(self.key_plugin)

    def run(self):
        cherrypy.quickstart(MainView(), "/", self.CONFIG)
    
    def stop_wsgi(self):
        print("Stopping the wsgi...")
        self.sa_plugin.stop()
        self.key_plugin.stop()
        cherrypy.engine.stop()
    
    def wsgi_application(self):
        import atexit
        import signal

        sys.stdout = sys.stderr

        cherrypy.config.update({"enviroment": "production"})

        atexit.register(self.stop_wsgi)
        # signal.signal(signal.SIGKILL, sigHandler)
        signal.signal(signal.SIGTERM, sigHandler)
        signal.signal(signal.SIGQUIT, sigHandler)

        self.sa_plugin.start()
        self.key_plugin.start()
        
        application = cherrypy.Application(
            MainView(), script_name='', config=self.CONFIG)

        return application

def sigHandler(signo, frame):
    print("Through signal")
    sys.exit(0)
