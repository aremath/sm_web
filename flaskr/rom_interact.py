# Python imports
import os, math, tempfile, json, signal, shutil, time, subprocess, sys
# Flask imports
from werkzeug.utils import secure_filename
# Personal imports
# Install github.com/aremath/sm_rando somewhere
tempfile.tempdir = "../instance"

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError

num_items = {
        "etanks":   (100, "E"),
        "missiles": (5, "M"),
        "supers":   (5, "S"),
        "pbs":      (5, "PB")
        }

check_items = {
        "charge":           "CB",
        "ice":              "IB",
        "wave":             "WB",
        "spazer":           "Spazer",
        "plasma":           "PLB",
        "varia":            "VS",
        "gravity":          "GS",
        "morph":            "MB",
        "bombs":            "B",
        "spring_ball":      "SPB",
        "screw":            "SA",
        "speed":            "SB",
        "hi_jump":          "HJB",
        "grapple":          "G",
        "xray":             "XR",
        }

# TRANSLATION

def mk_starting_items(request):
    start = ""
    for key in num_items:
        n = int(request[key])
        coef, name = num_items[key]
        amount = n * coef
        if key == "etanks":
            amount += 99
        if amount > 0:
            start += name
            start += str(amount)
            start += " "
    for key in check_items:
        if key in request:
            start += check_items[key]
            start += " "
    return start

N_MAJORS = 20
TOTAL_ITEMS = 100

def mk_item_placement(request):
    items_placed = 0
    placement = {}
    placement["extra"] = {}
    # Handle majors separately
    n_all = int(request["majors"])
    items_placed += n_all * N_MAJORS
    placement["starting"] = n_all
    for k in list(check_items.keys()):
        n = int(request[k + "place"])
        if n > 0:
            name = check_items[k]
            placement["extra"][name] = n
            items_placed += n
    # Set up the ratios dictionary
    # Handle reserve separately
    n_reserves = int(request["reserveplace"])
    ratios = {"RT": n_reserves}
    for k in num_items.keys():
        n = int(request[k + "place"])
        if n > 0:
            _, name = num_items[k]
            ratios[name] = n
    items_left = TOTAL_ITEMS - items_placed
    # Compute the actual number of each item
    item_place = mk_item_ratio(ratios, items_left)
    # Add it to the placement
    for k, v in item_place.items():
        placement["extra"][k] = v
    return placement

def mk_item_ratio(item_ratios, n_items):
    total = sum(item_ratios.values())
    # key, int - the integer "part" of each ratio
    int_vals = {}
    # key, float - the decimal "part" of each ratio
    dec_vals = {}
    left = total
    for k,v in item_ratios.items():
        ratio = float(v) / total
        n_float = ratio * n_items
        # The part after the decimal point
        n_decimal = n_float - math.floor(n_float)
        # The part before the decimal point
        n_int = int(n_float - n_decimal)
        left -= n_int
        int_vals[k] = n_int
        dec_vals[k] = n_decimal
        assert n_decimal < 1
        assert n_decimal >= 0
    # Now fix up the decimal values by distributing the rounded portion
    # in order of how much left each one has
    rounded_vals = {}
    for k,v in sorted(list(dec_vals.items()), key=lambda x: x[1], reverse=True):
        # If there's no rounding left, stop
        if left == 0:
            break
        else:
            rounded_vals[k] = 1
            left -= 1
    # Now put them together
    out = {}
    for k in item_ratios.keys():
        r_k = 0
        if k in rounded_vals:
            r_k = rounded_vals[k]
        out[k] = int_vals[k] + r_k
    return out

def mk_settings_from_request(request):
    starting_items = mk_starting_items(request)
    item_placement = mk_item_placement(request)
    return starting_items, item_placement

def setup_valid_rom(rom, request):
    save_name = secure_filename(rom.filename)
    save_folder = tempfile.mkdtemp()
    # Save the rom to the work directory
    rom.save(os.path.join(save_folder, save_name))
    return save_folder, save_name

def handle_valid_rom(rando_path, rel_path, form, save_folder, save_name, db, work_timeout, wait_timeout, err_timeout):
    # Hijack stdout for output
    logfile = os.path.join(save_folder, "logfile1")
    sys.stdout = open(logfile, "w")

    # Increment the number of folders and threads (respectively)
    if db is not None:
        #n_threads = int(db.execute("SELECT value FROM requests WHERE key = \"n\"").fetchone()[0])
        #print("T-N Threads: {}".format(n_threads))
        db.execute("UPDATE requests SET value = value + 1 WHERE key = \"n\"")
        db.execute("UPDATE requests SET value = value + 1 WHERE key = \"k\"")
        db.commit()
        #n_threads = int(db.execute("SELECT value FROM requests WHERE key = \"n\"").fetchone()[0])
        #print("T-N Threads: {}".format(n_threads))

    error = None

    # Work part
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(work_timeout)
    try:
        starting_items, item_placement = mk_settings_from_request(form)
        # Save the settings to the work directory
        settings_dir = os.path.join(save_folder, "settings")
        os.mkdir(settings_dir)
        with open(os.path.join(save_folder, "settings", "items.set"), "w") as setfile:
            json.dump(item_placement, setfile)

        os.mkdir(os.path.join(save_folder, "output"))
        # Relative save folder path for the rando alg
        b = os.path.basename(save_folder)
        rel_save_folder = os.path.join(rel_path, b)
        rel_logfile = os.path.join(rel_save_folder, "logfile2")
        args = [
                "--clean", os.path.join(rel_save_folder, save_name),
                "--create", os.path.join(rel_save_folder, "output", "rando_rom.smc"),
                "--graph",
                "--completable",
                "--starting_items", starting_items,
                "--settings", settings_dir,
                "--logfile", rel_logfile
                ]
        # Add other miscellanious flags
        seed = form["seed"]
        if seed != "":
            args.extend(["--seed", seed])
        if form["mode_preset"] == "hard":
            args.append("--hard_mode")
        if "noescape" in form:
            args.append("--noescape")
        if "g8" in form:
            args.append("--g8")
        # Actually call the thing
        #TODO: in the future, update directory structure to be able to import this file
        command = ["python3", "door_rando_main.py"] + args
        print(command)
        #TODO: timeout?
        returncode = subprocess.call(command, cwd=rando_path)
        if returncode < 0:
            error = "Error: Shell error {}".format(a)
    except TimeoutError:
        error = "Error: ROM generation timed out."
    except AssertionError:
        error = "Error: Assertion Error."
    #except Exception as e:
    #    print(e)
    #    error = "Unknown Error"

    # Decrement the number of threads
    # This thread no longer needs resources since it is no longer generating
    # So it does not count towards the limit
    if db is not None:
        db.execute("UPDATE requests SET value = value - 1 WHERE key = \"k\"")
        db.commit()

    print("Done")
    # Unset alarm
    signal.alarm(0)

    # Wait part
    if error is None:
        # Create done.txt
        d_path = os.path.join(save_folder, "done.txt")
        # Zip the directory
        shutil.make_archive(os.path.join(save_folder, "rando"), "zip", os.path.join(save_folder, "output"))
        with open(d_path, "w") as f:
            f.write("DONE")
            #json.dump(output, f)
        # Wait for the wait timeout
        time.sleep(wait_timeout)
    else:
        print(error)
        # Create error.txt
        e_path = os.path.join(save_folder, "error.txt")
        with open(e_path, "w") as f:
            f.write(error)
        time.sleep(err_timeout)
    
    # Clean up
    # Delete the directory
    shutil.rmtree(save_folder)
    # Decrement the number of folders
    if db is not None:
        db.execute("UPDATE requests SET value = value - 1 WHERE key = \"n\"")
        db.commit()
    return


