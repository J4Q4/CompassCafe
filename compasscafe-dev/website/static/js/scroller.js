// Lenis Button Scroll //
const lenis = new Lenis ({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
});

function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
}

requestAnimationFrame(raf);


// Reset Scroll Button //
// Recall jump to top button
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show button after scrolling 100px 
let resetButton = document.getElementById("resetButton");

// Button Animation
window.addEventListener('scroll', function() {
    if (window.scrollY > 100) {
        resetButton.classList.add("show-button");
    } else {
        resetButton.classList.remove("show-button");
    }
});




// Navbar Popup Animation
document.addEventListener('DOMContentLoaded', function() {
    let shownewnav = document.getElementById("nav-home");

    // Show after 600px
    window.addEventListener('scroll', function() {
        if (window.scrollY > 600) {
            shownewnav.classList.add("shownav");
        } else {
            shownewnav.classList.remove("shownav");
        }
    });
});