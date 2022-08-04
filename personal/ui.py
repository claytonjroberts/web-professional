"""User Interface elements for web application."""

# Core libs
import logging
import re
import sys
import uuid

# Third-party libs
from tornado.web import UIModule

# Source libs
from .constants import PATH_TEMPLATES
from .helpers import get_path_from_name


class HandlerUI(UIModule):
    """Base class for UI elements."""

    def render(self, name_directory: str = "ui", name_file=None):
        """Render the UI element."""
        self.id = str(uuid.uuid4()).replace("-", "")

        return self.render_string(
            (
                f"{name_directory}/"
                + get_path_from_name(
                    name=(self.__class__.title() if not name_file else name_file),
                    path=PATH_TEMPLATES / name_directory,
                ).name
            ),
            ui=self,
        )

    @classmethod
    def title(cls):
        return "_".join(cls.__name__.split("_")[1:]).lower()


# NOTE: SECTION -> DYNAMICALLY CREATED UIs
for path_template in [
    x
    for x in (PATH_TEMPLATES / "ui").iterdir()
    if (not x.is_dir() and re.search(r"\.html(?:\.j2)?", x.name, re.IGNORECASE))
]:
    # Dont worry about not including some, everything is controlled by the PH anyway
    # if not re.search("(old|new|_?test_?|_$)", f.stem, re.IGNORECASE):
    name_path_template = path_template.name.split(".")[0]

    # TODO: Add __admin for admin-only pages, add __auth for authenticated-only pages

    ui_name = "".join(
        [
            a if a.isupper() else b
            for a, b in zip(name_path_template, name_path_template.title())
        ]
    )

    _class_handler = type(f"UI_{ui_name}", (HandlerUI,), {})
    logging.info(f"Created ui {_class_handler}")
    setattr(sys.modules[__name__], _class_handler.__name__, _class_handler)


class UI_Vue(HandlerUI):
    """Vue.js UI element."""

    def render(self, name):
        # self.model = model
        return super().render(name_directory="vue", name_file=name)

    @property
    def splitName(self) -> str:
        matches = re.findall("[A-Z][a-z]+", self.model.__name__)
        return "-".join([str(x).lower() for x in matches])
