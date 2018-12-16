from multiprocessing import Process
from pathlib import Path
from threading import Thread

from pynpm import NPMPackage, YarnPackage
from pywebpack import WebpackProject

from personal.web.app import App

if __name__ == "__main__":

    # project_path = Path() / "static"
    # project = WebpackProject(project_path)
    # # project.install()
    # project.build()

    # pkg = NPMPackage((Path() / "package.json").absolute())
    # # # pkg.install()
    # # # pkg.build()
    # #
    # # # pkg.run_script("build")
    # p_pkg = Thread(target=pkg.run_script, args=("build",), daemon=True)

    # p_pkg.start()

    # pkg = NPMPackage((Path() / "package.json").absolute())
    # p_pkg = Thread(target=pkg.run_script, args=("build",), daemon=True)

    # a = App()
    # p_web = Thread(target=a.serve, args=())
    #
    # ps = [p_pkg, p_web]
    #
    # for p in ps:
    #     p.start()
    #
    # for p in ps:
    #     p.join()
    App().serve()

    # p_pkg.kill()
