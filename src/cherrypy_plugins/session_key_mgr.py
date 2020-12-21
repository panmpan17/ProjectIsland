import cherrypy
import os

from uuid import uuid1, uuid4
from threading import Timer
from datetime import datetime
from cherrypy.process.plugins import SimplePlugin

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
# WEEK = 7 * DAY
KEYTIMEOUT = DAY * 3  # become seconds


class ForgetPasswordData:
    CODE_EXPIRE = 1
    CODE_NOT_EXIST = 2

    ALREADY_EXIST = 3
    LOCK = 4

    def __init__(self, id_, email, code):
        self.id = id_
        self.email = email
        self.code = code
        self.time = datetime.utcnow()
        self.locked = False


class SessionKey:
    NOT_EXIST = 0
    TIMEOUT = 1
    ALREADY_LOGIN = 2
    SUCCESS = 3

    def __init__(self, key, user, time=None):
        self.key = key
        self.user = user

        if time is None:
            self.time = datetime.utcnow()
        else:
            self.time = time

    def __repr__(self):
        return f"<SessionKey '{self.key}' belongs to '{self.user}', create in '{self.time.strftime('%m/%d %H:%M:%S')}'>"


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
        self.is_running = False


class KeyMgrPlugin(SimplePlugin):
    def __init__(self, bus, path, interval=DAY):
        super().__init__(bus)
        self.keydict = {}
        # self.forget_pwds = []

        self.path = os.path.join(path, "keys")

        self.timer = RepeatedTimer(interval, self.clean_up_key)

    def start(self):
        if os.path.isfile(self.path):
            now = datetime.utcnow()

            with open(self.path) as f:
                line = f.readline()
                while line != "":
                    key, user, time = line.split(",")
                    user = int(user)
                    time = datetime.strptime(time[:-1], "%Y/%m/%d %H:%M:%S")

                    delta = (now - time).total_seconds()
                    if delta < KEYTIMEOUT:
                        self.keydict[key] = SessionKey(key, user, time)

                    line = f.readline()

        self.timer.start()

    def stop(self):
        with open(self.path, "w") as f:
            for key in self.keydict.values():
                time = key.time.strftime('%Y/%m/%d %H:%M:%S')
                f.write(
                    f"{key.key},{key.user},{time}\n")

        if self.timer is not None:
            self.timer.stop()

    def get_key(self, key):
        value = self.keydict.get(key)

        if value is not None:
            timedelta = datetime.utcnow() - value.time
            if timedelta.total_seconds() < KEYTIMEOUT:
                return value
            else:
                self.keydict.pop(key)
                return SessionKey.TIMEOUT
        else:
            return SessionKey.NOT_EXIST

    def add_key(self, requester, overwrite=False):
        # keys = list(self.keydict.keys())

        # for key in keys:
        #     if self.keydict[key].user == requester:
        #         if overwrite:
        #             self.keydict.pop(key)
        #         else:
        #             return SessionKey.ALREADY_LOGIN

        new_key = str(uuid1()).replace("-", "_")
        self.keydict[new_key] = SessionKey(new_key, requester)
        return new_key

    def drop_key(self, key):
        self.keydict.pop(key)

    def clean_up_key(self):
        print('start key cleaning')

        keys = []
        utcnow = datetime.utcnow()
        for k, i in self.keydict.items():
            timedelta = utcnow - i["date"]

            if timedelta.total_seconds() > KEYTIMEOUT:
                keys.append(k)

        for key in keys:
            self.keydict.pop(key)
            print(f"Key '{key}'' been delete")

    # def new_forget_pwd(self, id_, email):
    #     code = str(uuid4()).replace("-", "_")

    #     self.forget_pwds.append(ForgetPasswordData(
    #         id_, email, code))

    #     return code

    # def check_forget_pwd(self, id_):
    #     for data in self.forget_pwds:
    #         if data.id == id_:
    #             if data.locked:
    #                 return ForgetPasswordData.LOCK

    #             now = datetime.utcnow()
    #             if (now - data.time).total_seconds() > MINUTE * 5:
    #                 continue

    #             return ForgetPasswordData.ALREADY_EXIST
    #     return ForgetPasswordData.CODE_NOT_EXIST

    # def verify_forget_pwd(self, code):
    #     for data in self.forget_pwds:
    #         if data.code == code:
    #             now = datetime.utcnow()

    #             if (now - data.time).total_seconds() > HOUR:
    #                 return ForgetPasswordData.CODE_EXPIRE
    #             return data

    #     return ForgetPasswordData.CODE_NOT_EXIST

    # def lock_forget_pwd(self, code):
    #     for i, data in enumerate(self.forget_pwds):
    #         if data.code == code:
    #             data.locked = True
    #             return

    # def remove_forget_pwd(self, code):
    #     for i, data in enumerate(self.forget_pwds):
    #         if data.code == code:
    #             self.forget_pwds.pop(i)
    #             return


class KeyMgrTool(cherrypy.Tool):
    def __init__(self, key_plugin):
        cherrypy.Tool.__init__(self, "on_start_resource",
                               self.get_key_mgr, priority=10)
        self.key_plugin = key_plugin

    def get_plugin(self):
        return self.key_plugin

    def get_key_mgr(self):
        cherrypy.request.key = self.key_plugin
