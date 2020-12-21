import cherrypy
import random
import logging

from .model import WebsiteNewsSubscription, Account, AdminRole
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError


GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"

RECAPTCHA_SECRET = "6Lfouw0aAAAAAG9x7pkj5lfRiA3OzJ7uWASO1yBn"


class HTTPError(Exception):
    def __init__(self, status=400, msg=""):
        super().__init__()
        self.status = status
        self.msg = msg


def jsonlize(func):
    def wrapper(*args, **kwargs):
        result = None
        try:
            method = cherrypy.request.method

            if method == GET or method == DELETE:
                data = kwargs
            elif method == POST or method == PUT:
                data = cherrypy.request.json
            else:
                data = {}

            result = func(*args, method=method, data=data)
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

        except:
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
        "tools.keytool.on": True,
        "tools.encode.on": True,
    }


class RestMainView(View):
    def __init__(self):
        self.website_news_sub = WebsiteNewsSubscriptionView()
        self.account = AccountView()


class WebsiteNewsSubscriptionView(View):
    @cherrypy.expose
    @jsonlize
    def index(self, *args, method=None, data={}):
        if method == GET:
            subscriptions = []

            with cherrypy.request.db.session_scope() as session:
                for row in session.query(WebsiteNewsSubscription):
                    subscriptions.append(row.jsonlize())

            return {"data": subscriptions}

        elif method == POST:
            if "email" not in data:
                raise HTTPError(400)

            with cherrypy.request.db.session_scope() as session:
                new_subscribe = WebsiteNewsSubscription(
                    email=str(data["email"]), type=0,
                    ip=cherrypy.request.remote.ip)
                session.add(new_subscribe)

            return None
        
        raise HTTPError(404)
        # elif method == DELETE:
        #     with cherrypy.request.db.session_scope() as session:
        #         session.query(WebsiteNewsSubscription).delete()

        #     return None


class AccountView(View):
    @cherrypy.expose
    @jsonlize
    def index(self, *args, method=None, **kwargs):
        raise HTTPError(404)

    @cherrypy.expose
    @jsonlize
    def signup(self, *args, method=None, data={}):
        if method == POST:
            new_account = Account.new_from_data(data)

            with cherrypy.request.db.session_scope() as session:
                repeate_id_count = session.query(Account.id).filter(
                    Account.login_id == new_account.login_id).count()
                
                if repeate_id_count == 0:
                    session.add(new_account)
                else:
                    raise HTTPError(400, "Repeated login_id")

                session_key = cherrypy.request.key.add_key(new_account.id, True)

            return {"key": session_key}

        raise HTTPError(404)

    @cherrypy.expose
    @jsonlize
    def login(self, *args, method=None, data={}):
        if method == POST:
            if "login_id" not in data or "password" not in data:
                raise HTTPError(400)

            with cherrypy.request.db.session_scope() as session:
                account = session.query(Account).filter(
                    Account.login_id == data["login_id"]).first()

                if account is None:
                    raise HTTPError(400, "Field wrong")
                elif account.password != data["password"]:
                    raise HTTPError(400, "Field wrong")

                session_key = cherrypy.request.key.add_key(account.id, True)

            return {"key": session_key}

        raise HTTPError(404)
