# This file needs to be not named __main__ because it causes issues with Gunicorn

import os
from personal.web.app_tornado import App

app = App()

if __name__ == "__main__":
    app.serve(port=int(os.environ.get("PORT", 8000)))
