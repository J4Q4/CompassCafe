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




// Dashboard Popups
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
        const dropdown = this.closest('.dashboarduser-table');
        dropdown.style.zIndex = '3';
    });
    button.addEventListener('hidden.bs.dropdown', function() {
        // Find Parent of Dropdown - Card
        const dropdown = this.closest('.dashboarduser-table');
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
        accepted_application: `/apply/delete-duty/${itemId}`
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
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    } else {
        imagePreview.style.display = 'none';
    }
}


// Show Hovered Menu Item Details
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('mouseover', function() {
        const itemTitle = this.querySelector('h3').innerText;
        const itemPrice = this.querySelector('p').innerText;
        const itemImageSrc = this.querySelector('img').src;

        document.getElementById('hovered-item-title').innerText = itemTitle;
        document.getElementById('hovered-item-price').innerText = itemPrice;
        const itemImage = document.getElementById('hovered-item-image');
        itemImage.src = itemImageSrc;
        itemImage.style.display = 'block';
    });

    item.addEventListener('mouseout', function() {
        document.getElementById('hovered-item-image').style.display = 'none';
        document.getElementById('hovered-item-title').innerText = '';
        document.getElementById('hovered-item-price').innerText = '';
    });
});
