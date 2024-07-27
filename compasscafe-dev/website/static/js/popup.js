// Toggle Password Visibility //
function togglePassword() {
    var passwordField = document.getElementById("password");
    var confirmPasswordField = document.getElementById("confirm_password");
    var showPassword = document.getElementById("showPassword");
    if (showPassword.checked) {
        passwordField.type = "text";
        confirmPasswordField.type = "text";
    } else {
        passwordField.type = "password";
        confirmPasswordField.type = "password";
    }
}


// Dashboard Popup Filter //
document.addEventListener('DOMContentLoaded', (event) => {
    const popup = document.getElementById("filterjsPopup");
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


// Hide Spline Watermark //
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var splineViewer = document.querySelector('spline-viewer');
        if (splineViewer) {
            // Find Hidden Root [ Shadow DOM ]
            var shadowRoot = splineViewer.shadowRoot;
            if (shadowRoot) {
                var logo = shadowRoot.querySelector('a#logo');
                // Hide Watermark
                if (logo) {
                    logo.style.display = 'none';
                }
            }
        }
    }, 3300); // 3s Delay [ Give Load Time - Loadscreen ]
});