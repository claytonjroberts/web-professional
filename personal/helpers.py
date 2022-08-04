"""General helper functions."""

import re
from pathlib import Path


def get_path_from_name(name: str, path: Path) -> Path:
    """Get the path of a file from its name."""
    list_name_file_template = [
        pth
        for pth in path.iterdir()
        if (not pth.is_dir() and re.search(rf"^{name}\.", pth.name, re.IGNORECASE))
    ]

    if len(list_name_file_template) > 1:
        raise AssertionError(
            f"Multiple template files found for {name}: "
            f"{list_name_file_template} in {path}"
        )

    if len(list_name_file_template) == 0:
        raise AssertionError(f"No template files found for {name} in {path}")

    return list_name_file_template[0]
