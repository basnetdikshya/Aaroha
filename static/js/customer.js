document.addEventListener("DOMContentLoaded", function () {

    console.log("Aaroha Customer Portal Loaded");


    // ==========================================
    // Product Search
    // ==========================================
    const searchInput = document.querySelector("#customerSearch");

    const products = document.querySelectorAll(".product-card");

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue = this.value.toLowerCase();

            products.forEach(function (product) {

                const productName =
                    product.textContent.toLowerCase();

                product.style.display =
                    productName.includes(searchValue)
                        ? ""
                        : "none";

            });

        });

    }


    // ==========================================
    // Category Filter
    // ==========================================
    const categoryFilter =
        document.querySelector("#categoryFilter");

    if (categoryFilter) {

        categoryFilter.addEventListener("change", function () {

            const category = this.value.toLowerCase();

            products.forEach(function (product) {

                const productCategory =
                    product.dataset.category?.toLowerCase();

                if (
                    category === "all" ||
                    productCategory === category
                ) {
                    product.style.display = "";
                } else {
                    product.style.display = "none";
                }

            });

        });

    }


    // ==========================================
    // Add to Cart
    // ==========================================
    document.querySelectorAll(".add-cart-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            this.textContent = "Added ✓";

            setTimeout(() => {
                this.textContent = "Add to Cart";
            }, 1500);

        });

    });


    // ==========================================
    // Remove Cart Item
    // ==========================================
    document.querySelectorAll(".remove-cart-item").forEach(function (button) {

        button.addEventListener("click", function () {

            const confirmed = confirm(
                "Remove this product from your cart?"
            );

            if (confirmed) {

                const item =
                    this.closest(".cart-item");

                if (item) {
                    item.remove();
                }

            }

        });

    });


    // ==========================================
    // Checkout Confirmation
    // ==========================================
    const checkoutButton =
        document.querySelector("#checkoutButton");

    if (checkoutButton) {

        checkoutButton.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Do you want to place this order?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    }


    // ==========================================
    // Wishlist
    // ==========================================
    document.querySelectorAll(".wishlist-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            this.classList.toggle("active");

            if (this.classList.contains("active")) {
                this.textContent = "♥";
            } else {
                this.textContent = "♡";
            }

        });

    });

});