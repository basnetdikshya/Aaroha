document.addEventListener("DOMContentLoaded", function () {

    console.log("Aaroha Supplier Portal Loaded");


    // ==========================================
    // Purchase Request Search
    // ==========================================
    const searchInput =
        document.querySelector("#supplierSearch");

    const rows =
        document.querySelectorAll(".supplier-table tbody tr");

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue =
                this.value.toLowerCase();

            rows.forEach(function (row) {

                const text =
                    row.textContent.toLowerCase();

                row.style.display =
                    text.includes(searchValue)
                        ? ""
                        : "none";

            });

        });

    }


    // ==========================================
    // Quotation Form
    // ==========================================
    const quotationForm =
        document.querySelector("#quotationForm");

    if (quotationForm) {

        quotationForm.addEventListener("submit", function (event) {

            const price =
                document.querySelector("#quotationPrice");

            if (price && parseFloat(price.value) <= 0) {

                event.preventDefault();

                alert(
                    "Please enter a valid quotation price."
                );

                price.focus();
            }

        });

    }


    // ==========================================
    // Supply Confirmation
    // ==========================================
    document.querySelectorAll(".supply-confirm").forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Confirm that you are ready to supply this order?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ==========================================
    // Stock Quantity Validation
    // ==========================================
    document.querySelectorAll(".stock-input").forEach(function (input) {

        input.addEventListener("input", function () {

            if (parseInt(this.value) < 0) {
                this.value = 0;
            }

        });

    });


    // ==========================================
    // Status Display
    // ==========================================
    document.querySelectorAll(".order-status").forEach(function (status) {

        const value =
            status.textContent.trim().toLowerCase();

        status.classList.add(
            "status-" + value.replace(/\s+/g, "-")
        );

    });

});