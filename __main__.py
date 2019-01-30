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

if __name__ == "__main__":

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
