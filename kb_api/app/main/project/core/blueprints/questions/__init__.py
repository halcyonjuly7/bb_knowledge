from sanic import Blueprint

questions = Blueprint("questions")
from . import routes