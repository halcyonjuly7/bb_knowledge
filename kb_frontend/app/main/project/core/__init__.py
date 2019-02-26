from flask import Flask

def app_factory():
    app = Flask(__name__, static_folder="static")
    from .blueprints import home
    app.register_blueprint(home)

    from .blueprints import admin
    app.register_blueprint(admin, url_prefix="/admin")
    return app
