# Python imports
import multiprocessing

# Flask imports
from flask import render_template, Blueprint, request, current_app, redirect, flash

# Local imports
from . import config
from . import rom_interact
from flaskr.database import get_db

main_bp = Blueprint("main", __name__)

ROM_EXTENSIONS = ["smc", "sfc"]

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
    error = None
    # Error: Not a post request
    if request.method != "POST":
        return create_error("Not a POST")
    user_conf = request.form
    print(request.files)
    # Error: They didn't upload a ROM
    if "ROM" not in request.files:
        return create_error("No ROM")
    rom = request.files["ROM"]
    # Error: They didn't give the ROM a filename
    if rom.filename == "":
        return create_error("No ROM Filename")
    # Error: The ROM has a bad extension
    if not allowed_file(rom.filename, ROM_EXTENSIONS):
        return create_error("Bad ROM Extension")
    # Check the number of threads
    db = get_db()
    print(db)
    n_threads = db.execute("SELECT value FROM requests WHERE key = \"n\"").fetchone()
    print("N Threads: {}".format(int(n_threads[0])))
    # Error: Too many threads are running
    if int(n_threads[0]) >= current_app.config["MAX_THREADS"]:
        return create_error("Server is too busy")
    
    # If we get here, no errors
    #print(request.form)
    # First, set up the folder where we will process this request
    save_folder, save_name = rom_interact.setup_valid_rom(rom, request.form)
    #print(save_folder)
    # Now, spawn a new process to do the randomization and manage the files
    rpath = current_app.config["RANDO_PATH"]
    work_t = current_app.config["WORK_TIME"]
    wait_t = current_app.config["WAIT_TIME"]
    err_t = current_app.config["ERR_TIME"]
    p = multiprocessing.Process(target=rom_interact.handle_valid_rom,
            args=(rpath, request.form, save_folder, save_name, db, work_t, wait_t, err_t))
    p.start()
    # Finally, render the template
    return render_template("create.html", folder=save_folder)

def create_error(error):
    flash(error)
    return redirect(url_for("world_rando"))

@main_bp.route("/rogue")
def rogue_view():
    return render_template("rogue.html")

