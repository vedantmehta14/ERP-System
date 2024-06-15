window.addEventListener("load", function () {
    setTimeout(function () {
        let sidebar = document.querySelector(".sidebar");
        let closeBtn = document.querySelector("#btn");
        // let searchBtn = document.querySelector(".bx-search");

        closeBtn.addEventListener("click", () => {
            toggleSidebar();
        });

        // searchBtn.addEventListener("click", () => {
        //     toggleSidebar();
        // });

        function toggleSidebar() {
            sidebar.classList.toggle("open");
            sidebar.classList.toggle("closed");
            // menuBtnChange();

            // Save the sidebar state to local storage
            const isSidebarOpen = sidebar.classList.contains("open");
            localStorage.setItem("sidebarState", isSidebarOpen ? "open" : "closed");
        }

        // Restore the sidebar state from local storage when the page loads
        const savedSidebarState = localStorage.getItem("sidebarState");
        if (savedSidebarState === "open") {
            sidebar.classList.add("open");
        } else {
            sidebar.classList.add("closed");
        }
    }, 100);
});

function showConfirmationDialog() {
    document.getElementById('overlay').style.display = 'block';
    document.getElementById('confirmationModal').style.display = 'block';
}

function confirmLogout() {
    window.location.href = '/logout';
}

function cancelLogout() {
    hideConfirmationDialog();
}

function hideConfirmationDialog() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('confirmationModal').style.display = 'none';
}
