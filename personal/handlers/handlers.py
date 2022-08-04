"""Handlers for tornado."""

# Core libs
import json

# Source libs
from .base import HandlerAPI, HandlerPage


class PH_Logout(HandlerPage):
    """Logout handler."""

    def get(self):
        """Get the page."""
        # ModelHandler.Session.query(CM.UserAuthorization).filter_by(username=self.get_current_user_obj().username).delete()
        self.clear_cookie("userkey")
        self.redirect("/")


class API_Info(HandlerAPI):
    """API handler for info."""

    def get(self):
        """Get the page."""
        self.write(json.dumps(self.application.info, default=str))
