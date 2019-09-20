import inspect
import json
import re
import sys
from pathlib import Path

import tornado
import tornado.autoreload
import tornado.websocket
from tornado import gen

from ..core.console import ConsoleInterface


class Websocket(ConsoleInterface, tornado.websocket.WebSocketHandler):
    "Only one of these should be instanciated at a time"

    count = 0

    @gen.coroutine
    def open(self):
        self.application.addWebsocket(self)
        self.output("WebSocket opened [_]")
        self.chirp()

    @gen.coroutine
    def chirp(self):
        self.output("CAW")
        """Send message to client to update."""
        self.write_message("chirp")

    # @gen.coroutine
    # def on_message(self, message):
    #     # self.output("[RECIEVED] {}".format(message))
    #
    #     cargo = Cargo.loadData(message)
    #
    #     self.output("[RECIEVED] {}".format(cargo.__repr__()))
    #
    #     return self.send(self.application.parse(cargo, self))

    def on_close(self):
        self.output("WebSocket closed [X]")

    # @gen.coroutine
    # def send(self, cargo):
    #     try:
    #         assert(isinstance(cargo, Cargo))
    #     except AssertionError:
    #         print(type(cargo))
    #         quit()
    #     self.write_message(cargo.wrap())
    #     self.output("[SENT] {}".format(repr(cargo)))


class PageHandler(ConsoleInterface, tornado.web.RequestHandler):
    "Base class for request handlers"

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.output("[GET]")
        # print(self.request.headers.get("X-Real-IP"))
        self.render(
            "{}.html".format("_".join(self.__class__.__name__.split("_")[1:]).lower())
        )

    @classmethod
    def title(cls):
        return " ".join(cls.__name__.split("_")[1:]).lower()

    @classmethod
    def localUrl(cls):
        return "/{}".format("/".join(cls.__name__.lower().split("_")[1:]))

    def raiseError(self, error):
        """Set the error and re-load the page."""
        self.error = error
        self.get()

    def write_error(self, status_code, **kwargs):
        print("writing an error")

        if status_code == 404:
            return PH_Unauthorized.get()

        super().write_error(status_code, **kwargs)
        #
        # self.set_header('Content-Type', 'application/json')
        #
        # self.finish({
        #     'error': {
        #         'code': status_code,
        #         'message': self._reason,
        #     }
        # })

    # def error():
    #     doc = "The error property."
    #
    #     def fget(self):
    #         return self._error
    #
    #     def fset(self, value):
    #         if value is not None:
    #             self.output("[ERROR] {}".format(value))
    #         self._error = value
    #
    #     def fdel(self):
    #         del self._error
    #     return locals()
    # error = property(**error())

    # def initialize(self):
    #     """Set variables for PH."""
    #     self.ModelHandler = (
    #         ModelHandler()
    #     )  # TODO: Add ip or some identifying factor to the start of the ModelHandler object
    #     self.error = None

    @gen.coroutine
    def chirp(self):
        return self.application.chirp(self.user)


def doOutput(some_function):
    "Decorator"

    def wrapper(self, *args, **kwargs):
        self.output("[{}]".format(some_function.__name__.upper()))
        return some_function(self, *args, **kwargs)

    return wrapper


class API(PageHandler):
    @classmethod
    def localUrl(cls):
        return "/api{}".format(super().localUrl())


# CREATE PageHandlers based on what is in the templates folder
p = Path("templates").glob("*.html")
for x in p:
    l = x.stem
    if not re.search(r"(\Wold\W|\Wnew\W|(?:\w_)?test(?:_\w)?|_$)", l, re.IGNORECASE):
        # if not ('old' in l[-3:]
        #         or 'new' in l[-3:]
        #         or '_test' in l
        #         or '_' == l[-1]):

        tlist = x.stem
        t = "".join([a if a.isupper() else b for a, b in zip(tlist, tlist.title())])
        setattr(sys.modules[__name__], f"PH_{t}", type(f"PH_{t}", (PageHandler,), {}))
        print(f"{l}->{t}")

if __name__ == "__main__":
    pass
