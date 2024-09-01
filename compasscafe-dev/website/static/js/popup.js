// Toggle Password Visibility //
function togglePassword() {
    var passwordFieldID = ["password", "password1", "password2", "confirm_password"];
    var showPassword = document.getElementById("showPassword");
    
    passwordFieldID.forEach(function(id) {
        var passwordField = document.getElementById(id);
        if (passwordField) {
            passwordField.type = showPassword.checked ? "text" : "password";
        }
    });
}




// Dashboard + Menu Popups
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




// Mobile General Popups
document.addEventListener('DOMContentLoaded', () => {
    
    // Show Popup
    function togglePopup(popup) {
        if (popup.classList.contains("mobi-popupjs")) {
            popup.classList.remove("mobi-popupjs");
        } else {
            popup.classList.add("mobi-popupjs");
        }
    }

    // Click out of Range – Close Popup
    function closePopup(popup) {
        popup.classList.remove("mobi-popupjs");
    }
    // Sort Popup
    const mobilesortPopup = document.getElementById("mobile-sortjsPopup");
    const sortBtn = document.getElementById("sortPopBTN");
    const sortCloseBtn = document.getElementById("mobisortPopClose");

    sortBtn.addEventListener('click', () => {
        togglePopup(mobilesortPopup);
    });

    sortCloseBtn.addEventListener('click', () => {
        closePopup(mobilesortPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != sortBtn && !mobilesortPopup.contains(event.target)) {
            closePopup(mobilesortPopup);
        }
    });

    // Filter Popup
    const mobilefilterPopup = document.getElementById("mobile-filterjsPopup");
    const filterBtn = document.getElementById("filterPopBTN");
    const filterCloseBtn = document.getElementById("mobifilterPopClose");

    filterBtn.addEventListener('click', () => {
        togglePopup(mobilefilterPopup);
    });

    filterCloseBtn.addEventListener('click', () => {
        closePopup(mobilefilterPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != filterBtn && !mobilefilterPopup.contains(event.target)) {
            closePopup(mobilefilterPopup);
        }
    });

});




// Apply Popups
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

    // Apply Popup
    const applyPopup = document.getElementById("applyjsPopup");
    const applyBtn = document.getElementById("applyPopBTN");
    
    applyBtn.addEventListener('click', () => {
        togglePopup(applyPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != applyBtn && !applyPopup.contains(event.target)) {
            closePopup(applyPopup);
        }
    });
    
});




// Mobile Apply Popup
document.addEventListener('DOMContentLoaded', () => {
    
    // Show Popup
    function togglePopup(popup) {
        if (popup.classList.contains("mobi-popupjs")) {
            popup.classList.remove("mobi-popupjs");
        } else {
            popup.classList.add("mobi-popupjs");
        }
    }

    // Click out of Range – Close Popup
    function closePopup(popup) {
        popup.classList.remove("mobi-popupjs");
    }
    // Sort Popup
    const mobilesortPopup = document.getElementById("mobile-applyjsPopup");
    const mobileapplyBtn = document.getElementById("applyPopBTN");
    const mobileapplyCloseBtn = document.getElementById("filterPopClose");

    mobileapplyBtn.addEventListener('click', () => {
        togglePopup(mobilesortPopup);
    });

    mobileapplyCloseBtn.addEventListener('click', () => {
        closePopup(mobilesortPopup);
    });

    document.addEventListener('click', (event) => {
        if (event.target != mobileapplyBtn && !mobilesortPopup.contains(event.target)) {
            closePopup(mobilesortPopup);
        }
    });
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
    }, 100); // Progress Length //
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




// Dropdown Z-Index Fix
document.querySelectorAll('.dropdown-toggle').forEach(button => {
    button.addEventListener('click', function() {
        // Find Parent of Dropdown - Card
        const dropdown = this.closest('.dashboarduser-table, .menu-item-card');
        dropdown.style.zIndex = '3';
    });
    button.addEventListener('hidden.bs.dropdown', function() {
        // Find Parent of Dropdown - Card
        const dropdown = this.closest('.dashboarduser-table, .menu-item-card');
        dropdown.style.zIndex = '';
    });
});




// Confirm Delete Popup
function showDeletePopup(button) {
    // Delete
    const deleteForm = document.getElementById('delete-form');
    // User Display
    const descriptionSpan = document.getElementById('item-description');
    // Confirm Popup
    const confirmPopup = document.getElementById('confirm-popup');

    // If Error
    if (!deleteForm || !descriptionSpan || !confirmPopup) return;

    // Get User Attributes
    const itemType = button.getAttribute('data-item-type');
    const itemId = button.getAttribute('data-item-id');
    const itemDescription = button.getAttribute('data-item-description');

    // Types of Deletion
    const routes = {
        user: `/dashboard/delete_user/${itemId}`,
        pending_application: `/apply/delete-apply/${itemId}`,
        accepted_application: `/apply/delete-duty/${itemId}`,
        menu_item: `/menu/edit-item/delete-item/${itemId}`
    };

    deleteForm.action = routes[itemType] || '';
    descriptionSpan.textContent = itemDescription;
    // Show Popup
    confirmPopup.classList.add('show-delete-confirm');
}

// Close Popup
function closePopup() {
    document.getElementById('confirm-popup').classList.remove('show-delete-confirm');
}




// Show Accept Popup
function showAcceptPopup(button) {
    // Apply
    const acceptForm = document.getElementById('accept-form')
    // User Display
    const descriptionSpan = document.getElementById('accept-item-description');
    // Confirm Popup
    const confirmPopup = document.getElementById('confirm-accept-popup');

    // If Error
    if (!acceptForm || !descriptionSpan || !confirmPopup) return;

    // Get User Attributes
    const itemId = button.getAttribute('data-item-id');
    const itemDescription = button.getAttribute('data-item-description');

    acceptForm.action = `/apply/accept-apply/${itemId}`;
    descriptionSpan.textContent = itemDescription;
    // Show Popup
    confirmPopup.classList.add('show-delete-confirm');
}

// Close Popup
function closeAcceptPopup() {
    document.getElementById('confirm-accept-popup').classList.remove('show-delete-confirm');
}




// Menu File Selection
// Preview File Name
function showMenuFile() {
    var input = document.getElementById('image');
    var fileName = input.files[0] ? input.files[0].name : '';
    document.getElementById('file-name').textContent = fileName;
    
    // Preview Image
    var imagePreview = document.getElementById('image-preview');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(fileIMG) {
            imagePreview.src = fileIMG.target.result;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    } else {
        imagePreview.style.display = 'none';
    }
}


// Show Hovered Menu Item Details
document.querySelectorAll('.menu-item').forEach(item => {
    let hoverTimeout;

    item.addEventListener('mouseover', function() {
        hoverTimeout = setTimeout(() => {
            const hoveredItemDisplay = document.getElementById('hovered-item-display');
            hoveredItemDisplay.classList.add('show-hoverMenu');

            // Update content inside #hovered-item-display
            const itemTitle = this.querySelector('h3').innerText;
            const itemPrice = this.querySelector('p').innerText;
            const imgSrc = this.querySelector('img').src;
            const itemDescription = this.querySelector('h6').innerText;

            // Render the content
            document.getElementById('hovered-item-title').innerText = itemTitle;
            document.getElementById('hovered-item-price').innerText = itemPrice;
            document.getElementById('hovered-item-image').src = imgSrc;
            document.getElementById('hovered-item-description').innerText = itemDescription;
        }, 150); // 0.15s delay before showing image on hover
    });

    item.addEventListener('mouseout', function(event) {
        // Mouse Unhover Item
        if (!item.contains(event.relatedTarget)) {
            clearTimeout(hoverTimeout);
            const hoveredItemDisplay = document.getElementById('hovered-item-display');
            hoveredItemDisplay.classList.remove('show-hoverMenu');
        }
    });
});




// Show Menu Item Contents Popup
function showMenuDescPopup(button) {
    // Confirm Popup
    const confirmPopup = document.getElementById('menudesc-popup');

    // If Error
    if (!confirmPopup) return;

    // Get User Attributes
    const itemId = button.getAttribute('data-item-id');
    const itemImage = button.getAttribute('data-item-image');
    const itemTitle = button.getAttribute('data-item-title');
    const itemPrice = button.getAttribute('data-item-price');
    const itemDescription = button.getAttribute('data-item-description');

    // Set the popup content
    confirmPopup.querySelector('.popup-item-title').textContent = itemTitle;
    confirmPopup.querySelector('.popup-item-price').textContent = itemPrice;
    confirmPopup.querySelector('.popup-item-description').textContent = itemDescription;
    confirmPopup.querySelector('.popup-item-image').src = itemImage;

    // Show Popup
    confirmPopup.classList.add('show-delete-confirm');
}

// Close Popup
function closeMenuDescPopup() {
    document.getElementById('menudesc-popup').classList.remove('show-delete-confirm');
}
