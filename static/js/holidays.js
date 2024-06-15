function showForm() {
    document.getElementById('holidayOverlayForm').style.display = 'block';
    document.getElementById('holidayFormContent').style.display = 'block';
    applyfornewholiday(); // Call the function to generate leave ID and display the form
}

function cancelButton() {
    hideForm();
}

function hideForm() {
    document.getElementById('holidayOverlayForm').style.display = 'none';
    document.getElementById('holidayFormContent').style.display = 'none';
}