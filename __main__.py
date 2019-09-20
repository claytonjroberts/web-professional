from flask import Flask
import flask
from pathlib import Path
import yaml


app = Flask(
    __name__, template_folder=Path() / "templates", static_folder=Path() / "static"
)

with open(Path() / "info.yaml") as fh:
    app.info = yaml.load(fh, Loader=yaml.FullLoader)


@app.route("/")
def index():
    return flask.render_template("index_flask.html", app=app)


@app.route("/info", methods=["GET"])
def info():
    return app.info


# if __name__ == "__main__":
app.run(use_reloader=True, debug=True)
