import re
from pathlib import Path

REGEX_NAME_TERMS = re.compile(
    r"(?:(?<=[a-zA-Z])|(?<=^))([A-Z]+|[A-Z][a-z]+)(?:(?=[A-Z])|(?=$))"
)

PATH_TEMPLATES = Path() / "src" / "templates"

PATH_INFO = Path() / "data" / "info.yaml"
