#from . import rom_interact
import rom_interact
from flask import request
import tempfile, shutil, os

form = {
    "etanks":   "2",
    "missiles": "1",
    "supers":   "0",
    "pbs":      "0",
    "charge":   "on",
    "morph":    "on",
    "majors":   "1",
    "etanksplace":      "26",
    "missilesplace":    "18",
    "supersplace":      "17",
    "pbsplace":         "18",
    "reserveplace":     "0",
    "chargeplace":      "0",
    "waveplace":        "0",
    "iceplace":         "0",
    "spazerplace":      "0",
    "plasmaplace":      "0",
    "variaplace":       "0",
    "gravityplace":     "0",
    "morphplace":       "0",
    "bombsplace":       "0",
    "spring_ballplace": "0",
    "screwplace":       "0",
    "speedplace":       "0",
    "hi_jumpplace":     "0",
    "grappleplace":     "0",
    "xrayplace":        "0",
    "seed":             "",
    "noescape":         "",
    "g8":               "",
    "hard_mode":        ""
    }

rom = "/mnt/d/Ross/Programming/sm door rando/roms/sm_clean.smc"

def main():
    # Fake setup stuff
    fake_form = form
    save_folder = tempfile.mkdtemp()
    save_name = os.path.join(save_folder, "ayy.smc")
    shutil.copyfile(rom, save_name)
    rpath = "../../sm_rando/"
    # Do the thing
    rom_interact.handle_valid_rom(rpath, fake_form, save_folder, save_name, None, 180, 60, 60)
    return

if __name__ == "__main__":
    main()
