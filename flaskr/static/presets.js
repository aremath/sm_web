easy_preset = document.getElementById("easy_preset")
medium_preset = document.getElementById("medium_preset")
hard_preset = document.getElementById("hard_preset")
two_majors_preset = document.getElementById("two_majors_preset")
one_major_preset = document.getElementById("one_major_preset")
missile_bonanza_preset = document.getElementById("missile_bonanza_preset")
var ammos = ["etanks", "supers", "missiles", "pbs"]
var beams = ["charge", "wave", "ice", "spazer", "plasma"]
var suits = ["varia", "gravity"]
var items = ["morph", "bombs", "spring_ball", "screw", "speed", "hi_jump", "grapple", "xray"]

// preset lambda
preset_lambda_start = function (set_ammos, set_beams, set_suits, set_items) {
    var i;
    // Set the sliders
    for (i=0; i < ammos.length; i++) {
        var a = document.getElementById(ammos[i]);
        a.value = set_ammos[i];
        // update the counter as well
        var a_target = a.getAttribute("aria-controls");
        var thespan = document.getElementById(a_target);
        thespan.innerHTML = a.value;
    }
    // Set the checkboxes
    other_things = beams.concat(suits, items)
    set_other_things = set_beams.concat(set_suits, set_items)
    for (i=0; i < other_things.length; i++) {
        var a = document.getElementById(other_things[i]);
        a.checked = set_other_things[i];
    }
}
var easy_ammos = [4, 1, 2, 0];
var easy_beams = [true, false, false, true, false];
var easy_suits = [false, false];
var easy_items = [true, true, false, false, false, false, false, false];
easy_preset.onclick = function () {
    preset_lambda_start(easy_ammos, easy_beams, easy_suits, easy_items);
    return false;
}

var medium_ammos = [2, 0, 1, 0];
var medium_beams = [true, false, false, false, false];
var medium_suits = [false, false];
var medium_items = [true, false, false, false, false, false, false, false];
medium_preset.onclick = function () {
    preset_lambda_start(medium_ammos, medium_beams, medium_suits, medium_items);
    return false;
}

var hard_ammos = [1, 0, 0, 0];
var hard_beams = [false, false, false, false, false];
var hard_suits = [false, false];
var hard_items = [false, false, false, false, false, false, false, false];
hard_preset.onclick = function () {
    preset_lambda_start(hard_ammos, hard_beams, hard_suits, hard_items);
    return false;
}

preset_lambda_place = function(place_majors, place_ammos, place_beams, place_suits, place_items) {
    m = document.getElementById("majors")
    m.value = place_majors
    var m_target = m.getAttribute("aria-controls");
    var thespan = document.getElementById(m_target);
    thespan.innerHTML = m.value;

    ammos_r = ammos.concat(["reserve"])
    var all = ammos_r.concat(beams, suits, items)
    var all_place = place_ammos.concat(place_beams, place_suits, place_items);
    var i;
    // Set the sliders
    for (i=0; i < all.length; i++) {
        var a = document.getElementById(all[i] + "place");
        a.value = all_place[i];
        // update the counter as well
        var a_target = a.getAttribute("aria-controls");
        thespan = document.getElementById(a_target);
        thespan.innerHTML = a.value;
    }
}

var two_majors_majors = 2;
var two_majors_ammos = [22, 10, 12, 14, 0];
var two_majors_beams = [0, 0, 0, 0, 0];
var two_majors_suits = [0, 0];
var two_majors_items = [0, 0, 0, 0, 0, 0, 0, 0];
two_majors_preset.onclick = function () {
    preset_lambda_place(two_majors_majors, two_majors_ammos, two_majors_beams, two_majors_suits, two_majors_items);
    return false;
}

var one_major_majors = 1;
var one_major_ammos = [26, 17, 18, 18, 0];
var one_major_beams = [0, 0, 0, 0, 0];
var one_major_suits = [0, 0];
var one_major_items = [0, 0, 0, 0, 0, 0, 0, 0];
one_major_preset.onclick = function () {
    preset_lambda_place(one_major_majors, one_major_ammos, one_major_beams, one_major_suits, one_major_items);
    return false;
}

var missile_bonanza_majors = 1;
var missile_bonanza_ammos = [5, 2, 2, 2, 0];
var missile_bonanza_beams = [0, 0, 0, 0, 0];
var missile_bonanza_suits = [0, 0];
var missile_bonanza_items = [0, 0, 2, 0, 0, 0, 0, 0];
missile_bonanza_preset.onclick = function () {
    preset_lambda_place(missile_bonanza_majors, missile_bonanza_ammos, missile_bonanza_beams, missile_bonanza_suits, missile_bonanza_items);
    return false;
}

