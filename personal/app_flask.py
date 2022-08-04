from flask import Flask


class App(ConsoleInterface, Flask):
    """Master application"""

    def __init__(self):
        super()
        self.template_folder =

    def getHandlerList(self) -> list:
        handlers = [
            # (r"/ws", WH.Websocket),
            (r"/(.*)", WH.PH_Index),
            (
                r"/static/(.*)",
                tornado.web.StaticFileHandler,
                {"path": self.settings["static_path"]},
            ),
            # (
            #     r"/favicon.ico",
            #     tornado.web.StaticFileHandler,
            #     {
            #         "path": (
            #             self.settings["static_path"]
            #             / "src"
            #             / "images"
            #             / "favicon_io"
            #             # / "favicon.ico"
            #         )
            #     },
            # ),
        ]

        "Add all the pages by their names here."
        for y in inspect.getmembers(WH, inspect.isclass):
            x = y[1]
            if issubclass(x, WH.PageHandler) and x is not WH.PageHandler:
                # if issubclass(x, API) and x is not API:
                #     "API Handlers"
                #     handlers.append(
                #         ("/api{}".format(x.url_local()), x)
                #         )
                # else:
                #     "Page handlers"
                handlers.append(("{}".format(x.url_local()), x))
        [self.output("{:>30} -> {}".format(x[0], x[1].__name__)) for x in handlers]
        return handlers

    def __init__(self):
        # print(list(inspect.getmembers(sys.modules[__name__], inspect.isclass)))
        # "AUTORELOAD watch scss"
        # for file in [
        #     x for x in (Path(".") / "static" / "scss").iterdir() if not x.is_dir()
        # ]:
        #     tornado.autoreload.watch(file)
        #     # autoreload.watch(file)

        "Set tornado settings"
        self.settings = {
            "template_path": Path() / "templates",
            "static_path": Path() / "static",
            "ui_modules": ui_module,
            "debug": False,
            "login_url": "/login",
            "default_handler_class": WH.PH_Notfound,
        }

        # NOTE: Following not fully implemented yet
        # ssl_options = {"certfile": "cert.cer", "keyfile": "key.key"}

        # http_server = tornado.httpserver.HTTPServer(application, )

        cookie_secret = "Super secret cookie 4"  # TODO

        # self.websockets = set()
        with open(Path() / "info.yaml") as fh:
            self.info = yaml.load(fh, Loader=yaml.FullLoader)

        tornado.autoreload.watch(Path() / "info.yaml")
        tornado.web.Application.__init__(
            self, self.getHandlerList(), **self.settings, cookie_secret=cookie_secret
        )

    def addWebsocket(self, websocket):
        assert isinstance(websocket, WH.Websocket)
        self.websockets.add(websocket)

    def serve(self, port: int = 8000, isWSGI: bool = False):

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
        self.output(f"Starting at http://{ip}:{port}/")
        # self.output("Starting at port '{}'".format(port))

        if not isWSGI:
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
            raise

        # tornado.ioloop.IOLoop.current().stop()

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
