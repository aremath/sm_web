from flask import render_template, Blueprint, request
from . import config

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def main_view():
    return render_template("main.html")

@main_bp.route("/world_rando")
def world_rando_view():
    return render_template("world_rando.html", ammo=config.ammo, beams=config.beams, suits=config.suits, items=config.items)

@main_bp.route("/world_rando/create", methods=["POST"])
def create_view():
    if request.method == "POST":
        user_conf = request.form
        print(request.form)
        # spawn a thread to take care of the request
        # create a unique id to send to the website for download
        # generate a seed
        return render_template("create.html")

@main_bp.route("/rogue")
def rogue_view():
    return render_template("rogue.html")

