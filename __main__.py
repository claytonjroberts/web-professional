<<<<<<< HEAD
from flask import Flask
import flask
from pathlib import Path
import yaml
=======
# from multiprocessing import Process
# from pathlib import Path
# from threading import Thread

# from pynpm import NPMPackage, YarnPackage
# from pywebpack import WebpackProject

from personal.web.app import App

import tornado
import tornado.web
import tornado.wsgi
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # q = self.get_query_argument("q")
        # res = Pricing(q).pricing()
        self.write("hello")


global application
>>>>>>> 1344c7791c8721cc70d06349611ca3beaa7c018a

app = Flask(
    __name__, template_folder=Path() / "templates", static_folder=Path() / "static"
)

<<<<<<< HEAD
with open(Path() / "info.yaml") as fh:
    app.info = yaml.load(fh, Loader=yaml.FullLoader)


@app.route("/")
def index():
    return flask.render_template("index_flask.html", app=app)


@app.route("/info", methods=["GET"])
def info():
    return app.info


# if __name__ == "__main__":
app.run(use_reloader=True, debug=True)
=======
    # application = tornado.wsgi.WSGIAdapter(App())

    app = App()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

    # def make_app():
    #     return tornado.web.Application([(r"/", MainHandler)], debug=False)
    #
    # application = make_app()
    # application.listen(8080)
    # tornado.ioloop.IOLoop.current().start()

    # application = make_app()
    # application = tornado.wsgi.WSGIAdapter(application)
>>>>>>> 1344c7791c8721cc70d06349611ca3beaa7c018a
