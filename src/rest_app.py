import cherrypy
import random
import logging

from .model import WebsiteNewsSubscription
from sqlalchemy.sql import select


GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


class HTTPError(Exception):
    def __init__(self, status=400, msg=""):
        super().__init__()
        self.status = status
        self.msg = msg


def jsonlize(func):
    def wrapper(*args, **kwargs):
        result = None
        try:
            if "method" in kwargs:
                p_method = kwargs.pop("method")

            result = func(*args, method=cherrypy.request.method, **kwargs)
            if result is None:
                result = {}
            if "success" not in result:
                result["success"] = True

        except HTTPError as e:
            cherrypy.response.status = e.status
            result = {
                "success": False,
                "status_code": e.status,
                "reason": e.msg,
            }

            if e.status == 404:
                result["reason"] = "Page not found"

        except Exception as e:
            logging.exception("Caught server error")
            result = {
                "success": False,
                "status_code": 500,
                "reason": "Server unexpected error"
            }
            cherrypy.response.status = 500

        return result

    return wrapper


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
    @jsonlize
    def index(self, *args, method=None, **kwargs):
        if method == GET:
            data = []

            with cherrypy.request.db.session_scope() as session:
                for row in session.query(WebsiteNewsSubscription):
                    data.append(row.jsonlize())

            return {"data": data}

        elif method == POST:
            if "email" not in cherrypy.request.json:
                raise HTTPError(400)

            with cherrypy.request.db.session_scope() as session:
                new_subscribe = WebsiteNewsSubscription(email=str(cherrypy.request.json["email"]), type=0)
                session.add(new_subscribe)

            return None
        
        elif method == DELETE:
            with cherrypy.request.db.session_scope() as session:
                session.query(WebsiteNewsSubscription).delete()

            return None
