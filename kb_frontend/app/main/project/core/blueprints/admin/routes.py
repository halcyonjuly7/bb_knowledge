from . import admin
from flask import render_template

@admin.route("/", methods=["GET"])
def home():
    return render_template("admin_home.html")