from flask import render_template, Blueprint, request
from . import config
from . import rom_interact

main_bp = Blueprint("main", __name__)

ROM_EXTENSIONS = ["smc", "sfc"]
n_threads = 0
MAX_THREADS = 20

@main_bp.route("/")
def main_view():
    return render_template("main.html")

@main_bp.route("/world_rando")
def world_rando_view():
    return render_template("world_rando.html", ammo=config.ammo, beams=config.beams, suits=config.suits, items=config.items)

def allowed_file(filename, extensions):
    return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in extensions

@main_bp.route("/world_rando/create", methods=["POST"])
def create_view():
    if request.method == "POST":
        user_conf = request.form
        print(request.files)
        if "ROM" not in request.files:
            #flash("No ROM")
            print("No ROM")
        rom = request.files["ROM"]
        if rom.filename == "":
            #flash("No ROM 2")
            print("No ROM 2")
        if rom and allowed_file(rom.filename, ROM_EXTENSIONS) and n_threads < MAX_THREADS:
            # spawn a thread to take care of the request
            # create a unique id to send to the website for download
            # generate a seed
            print(request.form)
            print(rom.filename)
            rom_interact.handle_valid_rom(rom, request.form)
        return render_template("create.html")

@main_bp.route("/rogue")
def rogue_view():
    return render_template("rogue.html")

