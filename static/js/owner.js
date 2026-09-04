document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // Owner Dashboard
    // ==========================================
    console.log("Aaroha Owner Portal Loaded");


    // ==========================================
    // Sidebar Toggle
    // ==========================================
    const sidebarToggle = document.querySelector("#sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
        });
    }


    // ==========================================
    // Search Table
    // ==========================================
    const searchInput = document.querySelector("#ownerSearch");
    const tableRows = document.querySelectorAll(
        ".owner-table tbody tr"
    );

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue = this.value.toLowerCase();

            tableRows.forEach(function (row) {

                const rowText = row.textContent.toLowerCase();

                if (rowText.includes(searchValue)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });

        });

    }


    // ==========================================
    // Delete Confirmation
    // ==========================================
    document.querySelectorAll(".delete-btn").forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ==========================================
    // Report Filter
    // ==========================================
    const reportFilter = document.querySelector("#reportFilter");

    if (reportFilter) {

        reportFilter.addEventListener("change", function () {

            const selectedPeriod = this.value;

            console.log(
                "Owner report period:",
                selectedPeriod
            );

        });

    }


    // ==========================================
    // Notification Button
    // ==========================================
    const notificationButton =
        document.querySelector("#notificationButton");

    const notificationPanel =
        document.querySelector("#notificationPanel");

    if (notificationButton && notificationPanel) {

        notificationButton.addEventListener("click", function () {

            notificationPanel.classList.toggle("show");

        });

    }

});