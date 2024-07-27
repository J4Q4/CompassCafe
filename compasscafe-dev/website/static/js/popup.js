// Dashboard Popup //
document.addEventListener('DOMContentLoaded', (event) => {
    const popup = document.getElementById("myPopup");
    const btn = document.getElementById("filterPopBTN");

    // Declare Show Popup
    function showPopup() {
        popup.classList.add("dash-popupjs");
    }

    // Show Popup
    btn.onclick = function() {
        if (popup.classList.contains("dash-popupjs")) {
            popup.classList.remove("dash-popupjs");
        } else {
            showPopup();
        }
    }
    // Click out of Range – Close Popup
    window.onclick = function(event) {
        if (event.target !== btn && event.target !== popup && !popup.contains(event.target)) {
            popup.classList.remove("dash-popupjs");
        }
    }
});


