from core import app_factory
import os


if __name__ == "__main__":
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf", "dev.py")

    application = app_factory()

    application.run(host="0.0.0.0", port=5555, debug=True)