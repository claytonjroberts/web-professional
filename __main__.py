from pywebpack import WebpackProject
from pathlib import Path

if __name__ == "__main__":

    project_path = Path() / "static"
    # project = WebpackProject(project_path)
    # # project.install()
    # project.build()
    from pynpm import YarnPackage

    pkg = YarnPackage(Path() / "static" / "package.json")
    pkg.install()
    pkg.build()
