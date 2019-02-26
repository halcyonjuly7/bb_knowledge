import os

from core import app_factory

application = app_factory()

if __name__ == "__main__":
    app = app_factory()
    app.run(host="0.0.0.0", port=6666)




