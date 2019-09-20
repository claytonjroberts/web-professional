import re
import sys
import uuid
from pathlib import Path

from tornado.web import UIModule


class UI(UIModule):
    # def render(self, html=None, **kwargs):
    #     if html is None:
    #         html = self.__class__.__name__
    #     return self.render_string("ui/{}.html".format(html),
    #                               id=uuid.uuid4().__int__(), **kwargs)

    def render(self):
        self.id = str(uuid.uuid4()).replace("-", "")
        return self.render_string("ui/{}.html".format(self.__class__.title()), ui=self)

    @classmethod
    def title(cls):
        return "_".join(cls.__name__.split("_")[1:]).lower()


# NOTE: SECTION -> DYNAMICALLY CREATED UIs
for f in Path("templates/ui").glob("*.html"):
    # Dont worry about not including some, everything is controlled by the PH anyway
    # if not re.search("(old|new|_?test_?|_$)", f.stem, re.IGNORECASE):
    title_pre = f.stem.split("__")[0]
    title_tags = f.stem.split("__")[1:]
    # NOTE: Add __admin for admin-only pages, add __auth for authenticated-only pages

    t = "".join([a if a.isupper() else b for a, b in zip(title_pre, title_pre.title())])
    setattr(sys.modules[__name__], f"UI_{t}", type(f"UI_{t}", (UI,), {}))


class UI_Generic_Vue(UI):
    def render(self, model):
        self.model = model
        return super().render()

    @property
    def splitName(self) -> str:
        matches = re.findall("[A-Z][a-z]+", self.model.__name__)
        return "-".join([str(x).lower() for x in matches])
