from . import home
from flask import render_template, request

@home.route("/")
def home():
    return render_template("home.html")
