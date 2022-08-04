"""Base handlers for the Tornado web server."""

# Core Libs


# Third-party libs
import tornado
import tornado.autoreload
import tornado.websocket
from tornado import gen

# Source libs
from ..constants import PATH_TEMPLATES
from ..helpers import get_path_from_name


class HandlerPage(tornado.web.RequestHandler):
    """Base class for request handlers."""

    def __init__(self, *args, **kwargs):
        self.error = None
        super().__init__(*args, **kwargs)

    def data_received(self, chunk):
        """Override."""
        raise NotImplementedError

    @gen.coroutine
    def get(self, *args, **kwargs):
        """Get the page."""
        self.render(
            get_path_from_name(
                name="_".join(self.__class__.__name__.split("_")[1:]),
                path=PATH_TEMPLATES,
            ).name,
            **self.__class__.variables(),
        )

    @classmethod
    def variables(cls) -> dict:
        """Get varibles to pass into template."""
        return {}

    @classmethod
    def title(cls) -> str:
        """Get the title of the page."""
        return " ".join(cls.__name__.split("_")[1:]).lower()

    @classmethod
    def url_local(cls) -> str:
        """Get the local url for the page."""
        return "/" + "/".join(cls.__name__.lower().split("_")[1:])

    def raise_error(self, error):
        """Set the error and re-load the page."""
        self.error = error
        self.get()

    def write_error(self, status_code, **kwargs):
        """Write the error."""
        if status_code == 404:
            return PH_Unauthorized.get()

        super().write_error(status_code, **kwargs)

    def initialize(self):
        """Set variables for PH."""
        # self.ModelHandler = (
        #     ModelHandler()
        # )  # TODO: Add ip or some identifying factor to the start of the ModelHandler object
        self.error = None


class HandlerAPI(HandlerPage):
    """Base class for API handlers."""

    @classmethod
    def url_local(cls):
        """Get the local url for the page."""
        return f"/api{super().url_local()}"
