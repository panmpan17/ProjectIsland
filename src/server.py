import cherrypy

from .model import DatabaseManager
from .view_app import MainView


class Server:
    def __init__(self):
        DatabaseManager.to_sqlite("server.db")
        pass

    def run(self):
        DatabaseManager.connect_database()

        cherrypy.quickstart(MainView())

        DatabaseManager.dispose_engine()


def WSGIApplication():
    import sys
    import atexit

    sys.stdout = sys.stderr

    cherrypy.config.update({"enviroment": "embedded"})

    if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
        cherrypy.engine.start(blocking=False)
        atexit.register(cherrypy.engine.stop)
    
    application = cherrypy.Application(
        MainView(), script_name='', config=None)

    return application
