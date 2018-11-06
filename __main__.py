from pywebpack import WebpackProject
from pathlib import Path
from pynpm import YarnPackage, NPMPackage
from personal.web.app import App

if __name__ == "__main__":

    project_path = Path() / "static"
    # project = WebpackProject(project_path)
    # # project.install()
    # project.build()

    pkg = NPMPackage(Path() / "static" / "package.json")
    # pkg.install()
    # pkg.build()
    pkg.run_script("build")

    App().serve()
