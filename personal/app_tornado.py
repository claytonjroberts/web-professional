"""Main tornado application."""

# Core libs
import inspect
import logging
import socket
import typing
from pathlib import Path

import tornado
import tornado.autoreload
import tornado.web
import tornado.websocket
import tornado.wsgi
import yaml

from . import handlers as hd
from . import ui
from .constants import PATH_INFO


class App(tornado.web.Application):
    """Master tornado-based application."""

    def get_list_handlers(self) -> list:
        handlers = [
            (r"/", hd.PH_Index),
            # (
            #     r"/(favicon.ico)",
            #     tornado.web.StaticFileHandler,
            #     {"path": str(Path() / "static" / "favicon.ico")},
            # ),
        ]

        "Add all the pages by their names here."
        for handler_name, handler_cls in inspect.getmembers(hd, inspect.isclass):
            if (
                issubclass(handler_cls, hd.HandlerPage)
                and handler_cls is not hd.HandlerPage
            ):
                handlers.append((handler_cls.url_local(), handler_cls))

        for handler_name, handler_cls in handlers:
            logging.info(f"{handler_name :>30} -> {handler_cls.__name__}")

        return handlers

    def get_list_ui(self) -> typing.List[ui.HandlerUI]:
        uis = []

        "Add all the pages by their names here."
        for _, item in inspect.getmembers(ui, inspect.isclass):
            if issubclass(item, ui.HandlerUI) and item is not ui.HandlerUI:
                # if issubclass(x, API) and x is not API:
                #     "API Handlers"
                #     handlers.append(
                #         ("/api{}".format(x.url_local()), x)
                #         )
                # else:
                #     "Page handlers"
                uis.append(item)

        for item in uis:
            logging.info(f"{item !r} -> {item.__name__}")

        return uis

    def __init__(self):
        # print(list(inspect.getmembers(sys.modules[__name__], inspect.isclass)))
        # "AUTORELOAD watch scss"
        # for file in [
        #     x for x in (Path(".") / "static" / "scss").iterdir() if not x.is_dir()
        # ]:
        #     tornado.autoreload.watch(file)
        #     # autoreload.watch(file)

        # NOTE: Following not fully implemented yet
        # ssl_options = {"certfile": "cert.cer", "keyfile": "key.key"}

        # http_server = tornado.httpserver.HTTPServer(application, )

        with PATH_INFO.open() as fh:
            self.info = yaml.load(fh, Loader=yaml.FullLoader)

        # If information in info.yaml is changed, reload app
        tornado.autoreload.watch(Path() / "info.yaml")

        tornado.web.Application.__init__(
            self,
            self.get_list_handlers(),
            **{
                # Tornado settings
                "template_path": "src/templates",
                "static_path": "static",
                "ui_modules": ui,
                "debug": True,
                "login_url": "/login",
                "default_handler_class": hd.PH_NotFound,
            },
            cookie_secret="Super secret cookie 4",
        )

    def serve(self, port: int = 8080, is_wsgi: bool = False):
        """Start the server."""
        if tornado.ioloop.IOLoop.current():
            tornado.ioloop.IOLoop.current()

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
        logging.info(f"Starting at http://{ip}:{port}/")

        if not is_wsgi:
            server = tornado.httpserver.HTTPServer(self)
            # server.bind(int(port))
            # , ssl_options={
            #     "certfile": "cert.cer",
            #     "keyfile":  "key.key",
            # })
            server.listen(int(port))

            # self.startWebpack()

            # self.process_main = multiprocessing.Process(
            #     target=tornado.ioloop.IOLoop.current().start, args=()
            # )
            # self.process_main.start()
            try:
                tornado.ioloop.IOLoop.current().start()

            except KeyboardInterrupt:
                pass
                # self.process_webpack.stop()
        else:
            # wsgi_app = tornado.wsgi.WSGIAdapter(self)

            # server = wsgiref.simple_server.make_server("", 8888, wsgi_app)
            # server.serve_forever()
            raise Exception("Application is not WSGI compatible.")
