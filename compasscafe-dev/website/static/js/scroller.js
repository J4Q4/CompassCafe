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
        if (window.scrollY > 400) {
            shownewnav.classList.add("shownav");
        } else {
            shownewnav.classList.remove("shownav");
        }
    });
});


// Content Fade In on Scroll
document.addEventListener('DOMContentLoaded', function () {
    gsap.registerPlugin(ScrollTrigger);

    // Animate Container Contents
    gsap.utils.toArray('.fade-in div > *').forEach(function (fadeContent) {
        gsap.fromTo(fadeContent, 
            { 
                opacity: 0, 
                y: 50 
            }, 
            { 
                opacity: 1, 
                y: 0, 
                duration: 1, 
                delay: Math.random() * 0.5,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: fadeContent,
                    start: "top 100%",
                    toggleActions: "play none none none", 
                    once: true 
                }
            }
        );
    });
});



// Category Mobile Slider
function scrollLeftBtn() {
    const container = document.getElementById('category-list');
    const maxScrollLeft = container.scrollLeft;

    if (maxScrollLeft > 0) {
        container.scrollBy({ left: -200, behavior: 'smooth' });
    }
}

function scrollRightBtn() {
    const container = document.getElementById('category-list');
    container.scrollBy({ left: 200, behavior: 'smooth' });
}
