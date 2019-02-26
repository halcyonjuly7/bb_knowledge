from sanic import Blueprint

accounts = Blueprint("account")
from . import routes