import os, math
from werkzeug.utils import secure_filename

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
        out[k] = int_vals[k] + rounded_vals[k]
    return out

def mk_settings_from_request(request):
    starting_items = mk_starting_items(request)
    item_placement = mk_item_placement(request)
    return starting_items, item_placement

def handle_valid_rom(rom, request):
    starting_items, item_placement = mk_settings_from_request(request)
    print(starting_items)
    print(item_placement)
    save_name = secure_filename(rom.filename)
    #rom.save(os.path.join())

