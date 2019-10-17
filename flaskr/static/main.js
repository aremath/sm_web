// Handles sliders by usting the aria-controls attribut to find the
// counter to update
function slider_handler(e) {
    var target_element = e.target.getAttribute("aria-controls");
    var thespan = document.getElementById(target_element);
    thespan.innerHTML = e.target.value;
}

// Add it as a listener to the appropriate elements
var sliders = document.getElementsByClassName("slider")
for (let slider of sliders) {
    slider.oninput = slider_handler;
    // Set up initial state
    var target_element = slider.getAttribute("aria-controls");
    thespan = document.getElementById(target_element);
    thespan.innerHTML = slider.value;
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
