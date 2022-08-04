"""Tornado web handler factory."""

import logging
import re
import sys
from pathlib import Path

from ..constants import PATH_TEMPLATES
from .base import HandlerAPI, HandlerPage

# CREATE HandlerPages based on what is in the templates folder

for path_template in [
    x
    for x in PATH_TEMPLATES.iterdir()
    if (
        not x.is_dir()
        and re.search(r"\.html(?:\.j2)?", x.name, re.IGNORECASE)
        and not re.search(r"test.*\.", x.name, re.IGNORECASE)
    )
]:
    l = path_template.stem

    tlist = path_template.name.split(".")[0]
    handler_title = "".join(
        [a if a.isupper() else b for a, b in zip(tlist, tlist.title())]
    )

    _class_handler = type(f"PH_{handler_title}", (HandlerPage,), {})
    logging.info(f"Created handler {_class_handler}")

    setattr(sys.modules[__name__], _class_handler.__name__, _class_handler)

# Allow overwrite of handlers
from .handlers import *
