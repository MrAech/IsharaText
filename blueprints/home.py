from flask import Blueprint, render_template
from flask_login import login_required

homeBp = Blueprint("home", __name__, template_folder="templates")

@homeBp.route("/")
# @login_required
def home():
    return render_template("home.html")
