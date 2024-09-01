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




document.addEventListener('DOMContentLoaded', function () {
    // Initialise Splide Carousel
    var splide = new Splide('#image-carousel', {
        type   : 'loop',
        perPage: 3,
        perMove: 1,
        gap: '18rem',
        focus: 'center',
        pagination: false,
        arrows: false,
        speed: 500,
        breakpoints: {
            1400: { 
                perPage: 3,
                gap: '20rem',
            },
            1200: {
                perPage: 2,
                gap: '12rem',
            },
            992: {
                perPage: 2,
            },
            768: {
                perPage: 2,
                gap: '8rem',
            },
            576: {
                perPage: 1,
            },
        },
    }).mount();


    // Active Carousel Details - Mobile View
    var menuCarouselTitle = document.getElementById('menucarousel-title');
    var menuCarouselDescription = document.getElementById('menucarousel-description');
    var carouselInfo = document.getElementById('carousel-info');

    // Grab Carousel Info
    function updateSlideInfo() {
        var activeSlide = splide.Components.Slides.getAt(splide.index).slide;
        var title = activeSlide.getAttribute('data-title');
        var description = activeSlide.getAttribute('data-description');
        
        menuCarouselTitle.textContent = title;
        menuCarouselDescription.textContent = description;

        // CSS Active Animation
        carouselInfo.classList.add('active');
    }

    function hideSlideInfo() {
        // Remove CSS Active Animation
        carouselInfo.classList.remove('active');
    }

    splide.on('move', hideSlideInfo);

    splide.on('moved', function () {
        updateSlideInfo();
    });

    // Initial Animation Status Setup
    updateSlideInfo();
    carouselInfo.classList.add('active');


    // Custom Pagination
    var pagination = document.querySelector('#custom-pagination');
    var maxDots = 5;

    for (let i = 0; i < maxDots; i++) {
        var button = document.createElement('button');
        button.className = 'pagination-dot';
        button.type = 'button';

        // Event listener for pagination dot click
        button.addEventListener('click', () => splide.go(i));

        pagination.appendChild(button);
    }

    // Update Active Pagination Node
    splide.on('move', function () {
        document.querySelectorAll('.pagination-dot').forEach((dot, i) => {
            dot.classList.toggle('is-active', i === splide.index % maxDots);
        });
    });

    // Initialise Active Pagination Node
    splide.emit('move');
    
    // Previous Button
    document.querySelector('.splidebtn-menuprev').addEventListener('click', function () {
        splide.go('<');
    });

    // Next Button
    document.querySelector('.splidebtn-menunext').addEventListener('click', function () {
        splide.go('>');
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
                    start: "top 120%",
                    toggleActions: "play none none none", 
                    once: true 
                }
            }
        );
    });
});