import cherrypy
import random
import logging

from .model import WebsiteNewsSubscription, Account, AdminRole, ForumPost,\
    ForumReply
from .cherrypy_plugins import SessionKey
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

    @staticmethod
    def create_db_data_from_parameter(db_class, params):
        new_data = db_class()

        for c in db_class.__table__.columns:
            nullable = (c.default is not None) or c.nullable or c.primary_key

            if c.name not in params:
                if not nullable:
                    raise HTTPError(400, f"Parameter missing {c.name}")
            else:
                setattr(new_data, c.name, params[c.name])

        return new_data
    
    @staticmethod
    def check_session_key(data):
        if "key" not in data:
            raise HTTPError(401, "Missing Parameter key")

        key = cherrypy.request.key.get_key(data["key"])
        if key == SessionKey.NOT_EXIST:
            raise HTTPError(401, "Key is invalid")
        if key == SessionKey.TIMEOUT:
            raise HTTPError(401, "Key is invalid")

        return key

    @staticmethod
    def check_user_login(data):
        if "key" not in data:
            raise HTTPError(401, "Missing Parameter key")

        key = cherrypy.request.key.get_key(data["key"])
        if key == SessionKey.NOT_EXIST:
            raise HTTPError(401, "Key is invalid")
        if key == SessionKey.TIMEOUT:
            raise HTTPError(401, "Key is invalid")

        with cherrypy.request.db.session_scope(expire_on_commit=False) as session:
            account = session.query(Account).filter(
                Account.id == key.user).first()
            
        if account is None:
            raise HTTPError(400)

        return account


class RestMainView(View):
    def __init__(self):
        self.website_news_sub = WebsiteNewsSubscriptionView()
        self.account = AccountView()
        self.forum = ForumView()


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
    def index(self, *args, method=None, **kwargs):
        raise cherrypy.HTTPError(404)

    @cherrypy.expose
    @jsonlize
    def me(self, *args, method=None, data={}):
        if method == GET:
            return self.check_user_login(data).jsonlize(level=1)

        return None

    @cherrypy.expose
    @jsonlize
    def signup(self, *args, method=None, data={}):
        if method == POST:
            new_account = self.create_db_data_from_parameter(Account, data)

            with cherrypy.request.db.session_scope() as session:
                repeate_id_count = session.query(Account.id).filter(
                    Account.login_id == new_account.login_id).count()
                
                if repeate_id_count == 0:
                    session.add(new_account)
                    session.commit()
                    session_key = cherrypy.request.key.add_key(
                        new_account.id, True)
                else:
                    raise HTTPError(400, "Repeated login_id")

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


class ForumView(View):
    @cherrypy.expose
    def index(self, *args, **kwargs):
        raise cherrypy.HTTPError(404)

    @cherrypy.expose
    @jsonlize
    def post(self, *args, method=None, data={}):
        if method == GET:
            posts = []
            
            with cherrypy.request.db.session_scope() as session:
                for row in session.query(ForumPost):
                    posts.append(row.jsonlize())

            return {"data": posts}

        elif method == POST:
            key = self.check_session_key(data)

            data["author_account_id"] = key.user

            new_post = self.create_db_data_from_parameter(ForumPost, data)

            with cherrypy.request.db.session_scope() as session:
                session.add(new_post)

            return None
        
        raise HTTPError(404)

    @cherrypy.expose
    @jsonlize
    def reply(self, *args, method=None, data={}):
        if method == GET:
            if "post_id" not in data:
                raise HTTPError(400)

            replies = []

            with cherrypy.request.db.session_scope() as session:
                for row in session.query(ForumReply).filter(
                        ForumReply.post_id == data["post_id"]):
                    replies.append(row.jsonlize())

            return {"data": replies}
        
        elif method == POST:
            key = self.check_session_key(data)

            data["author_account_id"] = key.user

            new_reply = self.create_db_data_from_parameter(ForumReply, data)

            with cherrypy.request.db.session_scope() as session:
                session.add(new_reply)
            
            return None

        raise HTTPError(404)
