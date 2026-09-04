document.addEventListener("DOMContentLoaded", function () {

    console.log("Aaroha Staff Portal Loaded");


    // ==========================================
    // Product Search
    // ==========================================
    const searchInput = document.querySelector("#productSearch");

    const products = document.querySelectorAll(".product-card");

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue = this.value.toLowerCase();

            products.forEach(function (product) {

                const productName =
                    product.textContent.toLowerCase();

                if (productName.includes(searchValue)) {
                    product.style.display = "";
                } else {
                    product.style.display = "none";
                }

            });

        });

    }


    // ==========================================
    // Quantity Controls
    // ==========================================
    document.querySelectorAll(".quantity-control").forEach(function (control) {

        const minusButton =
            control.querySelector(".minus");

        const plusButton =
            control.querySelector(".plus");

        const quantity =
            control.querySelector(".quantity");

        if (plusButton && quantity) {

            plusButton.addEventListener("click", function () {

                let value = parseInt(quantity.value || quantity.textContent);

                value++;

                if (quantity.tagName === "INPUT") {
                    quantity.value = value;
                } else {
                    quantity.textContent = value;
                }

            });

        }


        if (minusButton && quantity) {

            minusButton.addEventListener("click", function () {

                let value = parseInt(quantity.value || quantity.textContent);

                if (value > 1) {
                    value--;
                }

                if (quantity.tagName === "INPUT") {
                    quantity.value = value;
                } else {
                    quantity.textContent = value;
                }

            });

        }

    });


    // ==========================================
    // Add to Order
    // ==========================================
    document.querySelectorAll(".add-order-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            this.textContent = "Added ✓";

            setTimeout(() => {
                this.textContent = "Add to Order";
            }, 1500);

        });

    });


    // ==========================================
    // Order Confirmation
    // ==========================================
    document.querySelectorAll(".confirm-order").forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to confirm this order?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ==========================================
    // Low Stock Highlight
    // ==========================================
    document.querySelectorAll(".stock-value").forEach(function (stock) {

        const value = parseInt(stock.textContent);

        if (!isNaN(value) && value <= 10) {
            stock.classList.add("low-stock");
        }

    });

});