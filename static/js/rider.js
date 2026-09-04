document.addEventListener("DOMContentLoaded", function () {

    console.log("Aaroha Delivery Rider Portal Loaded");


    // ==========================================
    // Delivery Search
    // ==========================================
    const searchInput =
        document.querySelector("#deliverySearch");

    const deliveries =
        document.querySelectorAll(".delivery-card");

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue =
                this.value.toLowerCase();

            deliveries.forEach(function (delivery) {

                const text =
                    delivery.textContent.toLowerCase();

                delivery.style.display =
                    text.includes(searchValue)
                        ? ""
                        : "none";

            });

        });

    }


    // ==========================================
    // Delivery Status
    // ==========================================
    document.querySelectorAll(".delivery-status").forEach(function (select) {

        select.addEventListener("change", function () {

            const status = this.value;

            const delivery =
                this.closest(".delivery-card");

            if (delivery) {

                const statusText =
                    delivery.querySelector(".status-text");

                if (statusText) {
                    statusText.textContent = status;
                }

            }

        });

    });


    // ==========================================
    // Confirm Delivery
    // ==========================================
    document.querySelectorAll(".complete-delivery").forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Confirm that this delivery has been completed?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ==========================================
    // Customer Contact
    // ==========================================
    document.querySelectorAll(".contact-customer").forEach(function (button) {

        button.addEventListener("click", function () {

            const phone =
                this.dataset.phone;

            if (phone) {

                window.location.href =
                    "tel:" + phone;

            }

        });

    });


    // ==========================================
    // Delivery Progress
    // ==========================================
    const progress =
        document.querySelector("#deliveryProgress");

    const statusSelect =
        document.querySelector("#deliveryStatus");

    if (progress && statusSelect) {

        statusSelect.addEventListener("change", function () {

            const status = this.value;

            if (status === "Assigned") {
                progress.value = 25;
            }

            else if (status === "Picked Up") {
                progress.value = 50;
            }

            else if (status === "On the Way") {
                progress.value = 75;
            }

            else if (status === "Delivered") {
                progress.value = 100;
            }

        });

    }

});