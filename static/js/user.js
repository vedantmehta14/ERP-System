function fetchUserData() {
    // Replace the following with your actual logic to fetch user data from the database
    const userData = {
        username: "vedant_mehta",
        email: "vedant.mehta@techsture.com",
        firstname: 'Vedant',
        middlename: 'Tushar',
        lastname: 'Mehta',
        address_line_1: '24, Arpan Society, Nr Mayur School',
        address_line_2: 'Paliyadnagar, Naranpura',
        city: 'Ahmedabad',
        pincode: '380013',
        state: 'Gujarat',
        country: 'India',
        dob: '14/01/2003',
        gender: 'Male',
        qualification: 'B. Tech',
        position: 'Intern',
        department: 'IT Services',
        reporting: 'Pathik Patel'
    };

    Object.keys(userData).forEach(key => {
        const value = userData[key];
        document.getElementById(key).textContent = value;
    });
}

function saveChanges() {
    // Add logic to save changes to the database
    // You can get the values from editable fields like this:
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;


    // Add your save changes logic here
    console.log("Changes saved:", newPassword, confirmPassword);
}


document.addEventListener("DOMContentLoaded", function () {
    // Fetch user data from the database
    fetchUserData();

    // Attach the file input change event listener
    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const profilePicture = document.getElementById('profile-picture');
                profilePicture.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});

function removeProfilePicture() {
    const profilePicture = document.getElementById('profile-picture');
    profilePicture.src = 'static/img/default.png';
}

function showPasswordFields() {
    // Show the password container when the button is clicked
    if (document.getElementById('password-container').style.display == 'none') {
        document.getElementById('password-container').style.display = 'block';
    } else {
        document.getElementById('password-container').style.display = 'none';
    }
}

function showAddressFields() {
    // Show the password container when the button is clicked
    if (document.getElementById('address-container').style.display == 'none') {
        document.getElementById('address-container').style.display = 'block';
    } else {
        document.getElementById('address-container').style.display = 'none';
    }
}

function saveChanges() {
    // Add logic to save changes (you can implement this based on your requirements)
    // For demonstration purposes, alert the values entered in the password fields
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    alert(`Current Password: ${currentPassword}\nNew Password: ${newPassword}\nConfirm Password: ${confirmPassword}`);
}

// Attach event listeners to buttons
document.getElementById('change-password-button').addEventListener('click', showPasswordFields);
document.getElementById('change-address-button').addEventListener('click', showAddressFields);
document.getElementById('save-changes-button').addEventListener('click', saveChanges);

function togglePasswordVisibility(inputId, eyeIconId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = document.getElementById(eyeIconId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('far', 'fa-eye-slash');
        eyeIcon.classList.add('far', 'fa-eye');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('far', 'fa-eye');
        eyeIcon.classList.add('far', 'fa-eye-slash');
    }
}



// var x = 0;
// function showHide() {
//     if(x==0) {
//         document.getElementById('text').style='display:none;';
//         x=1;    
//     } else {
//         document.getElementById('text').style='display:block;';
//         x=0;    
//     }
// }
