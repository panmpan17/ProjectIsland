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
