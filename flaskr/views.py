from flask import render_template, Blueprint
from . import config

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def main_view():
    return render_template("main.html")

@main_bp.route("/world_rando")
def world_rando_view():
    return render_template("world_rando.html", ammo=config.ammo, beams=config.beams, suits=config.suits, items=config.items)

@main_bp.route("/rogue")
def rogue_view():
    return render_template("rogue.html")
