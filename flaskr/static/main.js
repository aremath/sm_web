
// Handles dropdowns by using the aria-controls attribute to find the
// element to show
function dropdown_handler(e) {
    var target_element = e.target.getAttribute("aria-controls");
    var the_dropdown = document.getElementById(target_element);
    console.log(the_dropdown)
    the_dropdown.classList.toggle("show");
}

// Add it as a listener to the appropriate elements
// NOTE: requires that the <script> is placed last!
var btns = document.getElementsByClassName("dropbtn")
for (let btn of btns) {
    console.log(btn);
    btn.onclick = dropdown_handler;
}

window.onclick = function(e) {
    // Close all dropdowns if the user clicks outside them
    if (!e.target.matches(".dropbtn")) {
        var drops = document.getElementsByClassName("dropdown-content");
        console.log(drops);
        for (let drop of drops) {
            console.log(drop);
            console.log(drop.classList);
            if (drop.classList.contains("show")) {
                drop.classList.remove("show");
            }
        }
    }
}
