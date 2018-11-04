import inspect
import json
import re
import sys
from pathlib import Path

import markdown
import tornado
import tornado.autoreload
import tornado.websocket
from tornado import gen
from PRL_core.console import ConsoleInterface


class Websocket(ConsoleInterface, Mixin_User, tornado.websocket.WebSocketHandler):
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


class PageHandler(ConsoleInterface, Mixin_User, tornado.web.RequestHandler):
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

    def initialize(self):
        """Set variables for PH."""
        self.ModelHandler = (
            ModelHandler()
        )  # TODO: Add ip or some identifying factor to the start of the ModelHandler object
        self.error = None

    @gen.coroutine
    def chirp(self):
        return self.application.chirp(self.user)


def adminOnly(some_function):
    "Decorator"

    def wrapper(self, *args, **kwargs):
        if self.user.admin:
            return some_function(self, *args, **kwargs)
        else:
            return self.redirect(PH_Unauthorized.localUrl())

    return wrapper


def doOutput(some_function):
    "Decorator"

    def wrapper(self, *args, **kwargs):
        self.output("[{}]".format(some_function.__name__.upper()))
        return some_function(self, *args, **kwargs)

    return wrapper


class API(PageHandler):
    @tornado.web.authenticated
    def getCreature(self, id):
        return (
            self.ModelHandler.query(CM.Creature).filter_by(user=self.user, id=id).one()
        )

    @classmethod
    def localUrl(cls):
        return "/api{}".format(super().localUrl())


class API_ModelHandler(API):
    def getClassByTableName(self, tableName):
        cls = getattr(CM, tableName)

        if not self.user.admin and cls not in []:
            self.output(
                "[ERROR] {}".format(
                    "User {} is not allowed to access {}".format(self.user, cls)
                )
            )
            self.write_error()

        return cls

    @gen.coroutine
    @tornado.web.authenticated
    @doOutput
    def post(self):
        cls = self.getClassByTableName(self.get_argument("tableName"))

        data = {}
        for col in cls.__table__.columns:
            if self.get_argument(col.name, "") != "":
                data[col.name] = self.get_argument(col.name)

        "Add user data"
        if "userId" in [str(col.name) for col in cls.__table__.columns]:
            data["userId"] = self.user.id

        # if not func:
        try:
            self.ModelHandler.add(cls(**data))
        except sqlalchemy.exc.SQLAlchemyError as e:
            self.output("[ERROR] {}".format(e))
            self.write_error()

        # else:
        #     "Call the function"
        #     if func in cls._metallurgy.accessibles:

        self.chirp()
        self.finish()
        # self.redirect(PH_Admin.localUrl())

    @gen.coroutine
    @tornado.web.authenticated
    @doOutput
    def patch(self):
        """
        Philosophy: Patch should always have an id, tableName to get the object,
        and then the object should be manipulated (changed) by the columns it has.
        If I want to add a CreatureAbilities to a creature, I would target the
        tableName of CreatureAbilities, not Creature.
        """
        "Requires: tableName, id or func"
        cls = self.getClassByTableName(self.get_argument("tableName"))
        id = int(self.get_argument("id", None))

        func = self.get_argument("func", None)
        args = self.get_argument("args", None)
        # Args needs to be a dict, if not none
        assert isinstance(args, (type(None), dict)) or func is None

        data = {}
        for col in cls.__table__.columns:
            if self.get_argument(col.name, "") != "":
                data[col.name] = self.get_argument(col.name)

        self.output(f"[DATA] {data}")

        """Add user data (this needs to be after the data is added,
        just in case the user is not the same)"""
        # if "userId" in [str(col.name) for col in cls.__table__.columns]:
        #     data["userId"] = self.user.id

        if id:
            "Start object manipulation"
            obj = self.ModelHandler.query(cls).filter_by(id=id).one()

            if not func:
                for key, val in data.items():
                    setattr(obj, key, val)
            elif func in cls._metallurgy.accessibles:
                getattr(obj, func)(**args)
            else:
                self.write_error()

            self.ModelHandler.refresh(obj)

        else:
            "Start class function"
            obj = None

            if (
                func in cls._metallurgy.accessibles
                and cls._metallurgy.accessibles[func].__self__ is cls
            ):  # Assert that the func is a class method

                cls.cls._metallurgy.accessibles[func](**args)

        self.chirp()
        self.output(obj)  # obj will be none if it was a classmethod
        self.finish()

    @gen.coroutine  # No UserAuthorization because of index page
    @doOutput
    def get(self):
        self.output("[GET] (CALLED)")

        cls = self.getClassByTableName(self.get_argument("tableName"))

        data = {}
        for col in cls.__table__.columns:
            if self.get_argument(col.name, "") != "":
                data[col.name] = self.get_argument(col.name)

        "Add user data"
        if "userId" in [str(col.name) for col in cls.__table__.columns]:
            data["userId"] = self.user.id if self.user else None

        self.output("[GET] (Class={}) (Data={})".format(cls.__name__, data))

        # def object_as_dict(obj):
        #     with inspect as sqlalchemy.inspect:
        #         return {c.key: getattr(obj, c.key)
        #                 for c in inspect(obj).mapper.column_attrs}

        # rl = []
        # for x in l:
        #     try:
        #         rl.append(
        #             x.toDict()
        #         )
        #     except:
        #         print(x)
        #         print('-'*40)
        #         raise
        response = json.dumps(
            CM.Cargofy(
                cls.__name__,
                # object_as_dict(x) for
                [
                    x.toDict()
                    for x in sorted(
                        self.ModelHandler.query(cls).filter_by(**data).all()
                    )
                ],
            ).__dict__
        )

        self.output("[GET] (Response) {}".format(response))
        self.write(response)

        # try:
        #     self.write(
        #         # json.dumps([x.toDict() for x in list(self.ModelHandler.query(table).filter_by(**data).all())])
        #         json.dumps([x.toDict() for x in list(self.ModelHandler.query(cls).filter_by(**data).all())])
        #     )
        #     self.output(json.dumps([x.toDict() for x in list(self.ModelHandler.query(cls).filter_by(**data).all())]))
        # except sqlalchemy.exc.SQLAlchemyError as e:
        #     self.output("[ERROR] {}".format(e))
        #     self.write_error()

        # self.redirect(PH_Admin.localUrl())

    @gen.coroutine
    @tornado.web.authenticated
    @doOutput
    def delete(self):
        cls = self.getClassByTableName(self.get_argument("tableName"))

        print(cls)

        data = {}
        for col in cls.__table__.columns:
            if self.get_argument(col.name, "") != "":
                data[col.name] = self.get_argument(col.name)

        "Add user data"
        if "userId" in [str(col.name) for col in cls.__table__.columns]:
            data["userId"] = self.user.id if self.user else None

        self.output("(DATA) {}".format(data))

        items = self.ModelHandler.query(cls).filter_by(**data).all()

        self.output("(DELETING) {}".format(list(items)))

        self.ModelHandler.delete(*items)

        self.chirp()
        self.finish()


class API_Login(API):
    @gen.coroutine
    def post(self):
        # username = self.get_argument("username", "")
        # email = self.get_argument("email", "")

        password = self.get_argument("password", None)
        name = self.get_argument("name", None)
        email = self.get_argument("email", None)

        if "@" in email:
            assert re.match("[\d\w]+@cisco.com", email, re.IGNORECASE)

        login = json.loads(self.get_argument("login", True))

        # try:
        assert isinstance(login, bool)
        # except AssertionError:
        #     raise

        if login:
            self.output("LOGIN")

            try:
                key = self.application.user_login(email=email, password=password)
            except Exception as e:
                "Exit and re-render with error"
                raise tornado.web.HTTPError(status_code=e.code, message=e.args[0])
                # self.write_error(e.args[0])
            else:
                self.set_secure_cookie("userkey", tornado.escape.json_encode(key))
        else:  # Register
            self.output("REGISTER")

            if not all([email, name, password]):
                print([email, name, password])
                self.raiseError()

            if (
                ModelHandler.Session.query(CM.User).filter_by(email=email).first()
                is not None
            ):
                self.raiseError("Email already taken.")

            else:
                self.ModelHandler.add(
                    CM.User(email=email, password=password, name=name)
                )

                key = self.application.user_login(email=email, password=password)

                self.set_secure_cookie("userkey", tornado.escape.json_encode(key))


class API_Login_UserExists(API):
    @gen.coroutine
    def get(self):
        self.output("[GET]")
        # self.output(self.get_argument("test"))
        d = json.loads(self.get_argument("data"))

        # self.output(json.loads(self.request.arguments))
        # self.output(self.request.arguments["args"])
        # response = json.dumps(
        #     {"data": bool(self.ModelHandler.query(CM.User).filter_by(
        #         email=d['args']['email']).one_or_none())}
        #     )
        response = json.dumps(
            {"data": CM.User.exists(self.ModelHandler.session, **d["args"])}
        )
        self.output(response)
        self.write(response)
        self.finish()


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


class PH_Dashboard(PageHandler):
    @tornado.web.authenticated
    def get(self):
        super().get()


class PH_Logout(PageHandler):
    def get(self):
        # ModelHandler.Session.query(CM.UserAuthorization).filter_by(username=self.get_current_user_obj().username).delete()
        self.clear_cookie("userkey")
        self.redirect("/")


class PH_Admin(PageHandler):
    @tornado.web.authenticated
    @adminOnly
    def get(self):
        return super().get()

    @property
    def adminPHClasses(self):
        final = []
        for y in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            x = y[1]
            if issubclass(x, PH_Admin) and x is not PH_Admin:
                final.append(x)
        return final

    @classmethod
    def getDescription(cls):
        return NotImplementedError

    @classmethod
    def getIsTool(cls):
        return issubclass(cls, API)


class PH_Readme(PageHandler):
    def get(self):
        with open(Path("README.md"), "r") as fh:
            md = fh.read()
        self.fragment = markdown.markdown(md, extensions=["extra"])
        super().get()


if __name__ == "__main__":
    pass
