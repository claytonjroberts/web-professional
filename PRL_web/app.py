import inspect
import json
import re
import socket
import sys
import time
import uuid
from pathlib import Path

import sqlalchemy
import tornado
import tornado.autoreload
import tornado.websocket
from sqlalchemy import func, or_
from tornado import gen
from tornado.ioloop import IOLoop, PeriodicCallback

import CIS_data.models as CM
from CIS_core import ConsoleInterface
from CIS_data.handler import ModelHandler

from . import handlers as WH
from . import ui as ui_module


class Cisco_Exception(Exception):
    @property
    def code(self):
        return 400


class Mixin_User:
    def get_current_user_obj(self):
        return self.user

    def get_current_user(self):
        uo = self.user
        return uo.toDict() if uo is not None else None

    @property
    def user(self):
        if self.get_secure_cookie("userkey") is not None:
            key = tornado.escape.json_decode(self.get_secure_cookie("userkey"))
        else:
            return None
        try:
            q = self.ModelHandler.query(CM.UserAuthorization).filter_by(key=key).one()
        except sqlalchemy.orm.exc.NoResultFound:
            self.clear_cookie("userkey")
            return None
            # self.redirect(PH_Login.localUrl())
        else:
            return q.user


class Web_App(ConsoleInterface, tornado.web.Application):
    """Master application"""

    def getHandlerList(self) -> list:
        handlers = [(r"/ws", WH.Websocket), (r"/", WH.PH_Index)]

        "Add all the pages by their names here."
        for y in inspect.getmembers(WH, inspect.isclass):
            x = y[1]
            if issubclass(x, WH.PageHandler) and x is not WH.PageHandler:
                # if issubclass(x, API) and x is not API:
                #     "API Handlers"
                #     handlers.append(
                #         ("/api{}".format(x.localUrl()), x)
                #         )
                # else:
                #     "Page handlers"
                handlers.append(("{}".format(x.localUrl()), x))
        [self.output("{:>30} -> {}".format(x[0], x[1].__name__)) for x in handlers]
        return handlers

    def __init__(self):
        # print(list(inspect.getmembers(sys.modules[__name__], inspect.isclass)))
        "AUTORELOAD watch scss"
        for file in [
            x for x in (Path(".") / "static" / "scss").iterdir() if not x.is_dir()
        ]:
            tornado.autoreload.watch(file)
            # autoreload.watch(file)

        "Set tornado settings"
        settings = {
            "template_path": "templates",
            "static_path": "static",
            "ui_modules": ui_module,
            "debug": True,
            "login_url": "/login",
            "default_handler_class": WH.PH_Notfound,
        }

        # NOTE: Following not fully implemented yet
        ssl_options = {"certfile": "cert.cer", "keyfile": "key.key"}

        # http_server = tornado.httpserver.HTTPServer(application, )

        cookie_secret = "Super secret cookie 4"  # TODO

        # self.websockets = set()

        tornado.web.Application.__init__(
            self, self.getHandlerList(), **settings, cookie_secret=cookie_secret
        )

    def user_login(self, email, password):
        try:
            user = (
                ModelHandler.Session.query(CM.User)
                .filter(func.lower(CM.User.email) == email.lower())
                .one()
            )
        except sqlalchemy.orm.exc.NoResultFound:
            raise  # Exception_Login_UserNotFound(email)
        else:
            if user.password != password:
                raise  # Exception_InvalidPassword(email, password)
            else:
                "Create an api key to return"
                key = str(uuid.uuid1())
                # ModelHandler.Session.query(CM.UserAuthorization).filter_by(username=user.username).all.delete()
                # ModelHandler.Session.add(
                ua = CM.UserAuthorization(userId=user.id, key=key)
                # input(dir(ua))
                # ua.userId = user.id
                ModelHandler.Session.add(ua)
                return ua.key

    def addWebsocket(self, websocket):
        assert isinstance(websocket, WH.Websocket)
        self.websockets.add(websocket)

    # def parse(self, cargo, websocket):
    #     """
    #     Main method for api.
    #     :returns Cargo
    #     """
    #
    #     if cargo.call.lower() == "login" or cargo.key is None:
    #         websocket.user = User(**cargo.args)
    #
    #         cargo.key = websocket.user.key
    #         return Cargo.makeResponse(cargo, data={"key": cargo.key})
    #     else:
    #         "Find user, execute function"
    #         try:
    #             func = websocket.user.__getattribute__(cargo.call)
    #         except AttributeError:
    #             raise  # INVALID CALL
    #
    #         return Cargo.makeResponse(
    #             cargo, data=(func(**cargo.args)
    #                          if isinstance(cargo.args, dict) else func())
    #             )

    # if c.call == "login":
    #     return Cargo.makeResponse(requestCargo = c, data=API(**c.args).login())
    # else:
    #     if c.call in [x.__name__ for x in User.usableMethods]:
    #         return Cargo.makeResponse(requestCargo = c, data=)
    #     print(c.call)
    #     print(c.__repr__())

    def serve(self, port=8000):
        ip = (
            (
                [
                    ip
                    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                    if not ip.startswith("127.")
                ]
                or [
                    [
                        (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                    ][0][1]
                ]
            )
            + ["no IP found"]
        )[0]
        self.output(f"Starting at http://{ip}:{port}/")
        # self.output("Starting at port '{}'".format(port))
        server = tornado.httpserver.HTTPServer(self)
        # , ssl_options={
        #     "certfile": "cert.cer",
        #     "keyfile":  "key.key",
        # })
        server.listen(int(port))
        # PeriodicCallback(task, 1000).start()
        tornado.ioloop.IOLoop.instance().start()

    @gen.coroutine
    def chirp(self, user):
        """Look at all websockets and have them relay chirp if the client needs to be updated"""
        # If the user is in a campaign, update all users in that campaign, otherwise, chirp

        if not self.settings.get("debug", False):
            for x in self.websockets:
                if x.user == user:
                    return x.chirp()

        else:
            # DEBUG ONLY: chirp everywhere
            for x in self.websockets:
                x.chirp()
