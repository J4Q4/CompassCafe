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




document.addEventListener('DOMContentLoaded', () => {
    
    // Show Popup
    function togglePopup(popup) {
        if (popup.classList.contains("dash-popupjs")) {
            popup.classList.remove("dash-popupjs");
        } else {
            popup.classList.add("dash-popupjs");
        }
    }

    // Click out of Range – Close Popup
    function closePopup(popup) {
        popup.classList.remove("dash-popupjs");
    }

    
    // Sort Popup
    const sortPopup = document.getElementById("sortjsPopup");
    const sortBtn = document.getElementById("sortPopBTN");

    sortBtn.addEventListener('click', () => {
        togglePopup(sortPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != sortBtn && !sortPopup.contains(event.target)) {
            closePopup(sortPopup);
        }
    });

    // Filter Popup
    const filterPopup = document.getElementById("filterjsPopup");
    const filterBtn = document.getElementById("filterPopBTN");

    filterBtn.addEventListener('click', () => {
        togglePopup(filterPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != filterBtn && !filterPopup.contains(event.target)) {
            closePopup(filterPopup);
        }
    });

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
    }, 2500); // 2s Delay to Hide Watermark
});




// Preload Progress Bar //
document.addEventListener('DOMContentLoaded', function() {
    var progressBar = document.getElementById('progressBar');
    var progress = 0;
    var interval = setInterval(function() {
        progress += 10;
        // Visuals //
        progressBar.style.width = progress + '%';
        progressBar.innerText = progress + '%';
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 300); // Progress Length //
  });




// GSAP Onclick Animation - Sidebar Stagger //
document.querySelector('.sideToggle1')
.addEventListener('click', function() {
gsap.fromTo(".sideText1", 
    { // From
        right: '-150px', 
        opacity: 0 
    },
    { // To
        right: 0, 
        opacity: 1, 
        duration: 0.8, 
        stagger: 0.2, 
        ease: 'back' 
    }
);
});
// GSAP Onclick Animation - Sidebar Stagger //
document.querySelector('.sideToggle')
.addEventListener('click', function() {
gsap.fromTo(".sideText", 
    { // From
        right: '-150px', 
        opacity: 0 
    },
    { // To
        right: 0, 
        opacity: 1, 
        duration: 0.8, 
        stagger: 0.2, 
        ease: 'back' 
    }
);
});