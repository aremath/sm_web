
var event_types = ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"];

function set_input_filter(element, filter) {
    event_types.forEach(function (event) {
        element.addEventListener(event, function () {
            if (filter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            }
        });
    });
}

var intinputs = document.getElementsByClassName("intinput");

function intinput_handler(e) {
    var target_element = e.target.getAttribute("aria-controls");
    var theslider = document.getElementById(target_element);
    theslider.value = e.target.value
}

for (let intinput of intinputs) {
    set_input_filter(intinput, function(value) {
        return /^\d*$/.test(value) && (value === "" || (parseInt(value) >= intinput.min && parseInt(value) <= intinput.max)); });
    intinput.onchange = intinput_handler;
}

// Make intboxes only allow ints

// Handles sliders by usting the aria-controls attribut to find the
// counter to update
function slider_handler(e) {
    var target_element = e.target.getAttribute("aria-controls");
    var thespan = document.getElementById(target_element);
    thespan.value = e.target.value;
}

// Add it as a listener to the appropriate elements
var sliders = document.getElementsByClassName("slider")
for (let slider of sliders) {
    slider.oninput = slider_handler;
    // Set up initial state
    var target_element = slider.getAttribute("aria-controls");
    thespan = document.getElementById(target_element);
    thespan.value = slider.value;
}

// Handles dropdowns by using the aria-controls attribute to find the
// element to show
function dropdown_handler(e) {
    var target_element = e.target.getAttribute("aria-controls");
    var the_dropdown = document.getElementById(target_element);
    the_dropdown.classList.toggle("show");
}

// Add it as a listener to the appropriate elements
// NOTE: requires that the <script> is placed last!
var btns = document.getElementsByClassName("dropbtn")
for (let btn of btns) {
    btn.onclick = dropdown_handler;
}

window.onclick = function(e) {
    // Close all dropdowns if the user clicks outside them
    if (!e.target.matches(".dropbtn")) {
        var drops = document.getElementsByClassName("dropdown-content");
        for (let drop of drops) {
            if (drop.classList.contains("show")) {
                drop.classList.remove("show");
            }
        }
    }
}
