/* =====================================================
   AAROHA MAIN JAVASCRIPT
===================================================== */


/* =====================================================
   MOBILE NAVIGATION
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const menuButton =
        document.getElementById("mobileMenuButton");

    const navbarMenu =
        document.getElementById("navbarMenu");


    if (menuButton && navbarMenu) {

        menuButton.addEventListener("click", function () {

            const isOpen =
                navbarMenu.classList.toggle("show");


            menuButton.setAttribute(
                "aria-expanded",
                isOpen
            );

        });

    }

});


/* =====================================================
   PURCHASE MANAGEMENT
===================================================== */

function addPurchaseItem() {

    const container = document.getElementById(
        'purchase-items'
    );

    const firstRow = document.querySelector(
        '.purchase-item-row'
    );

    if (!container || !firstRow) {
        return;
    }

    const newRow = firstRow.cloneNode(true);

    newRow.querySelectorAll('input').forEach(
        input => {
            input.value = '';
        }
    );

    newRow.querySelectorAll('select').forEach(
        select => {
            select.selectedIndex = 0;
        }
    );

    container.appendChild(newRow);

    updatePurchaseTotal();
}


function removePurchaseItem(button) {

    const rows = document.querySelectorAll(
        '.purchase-item-row'
    );

    if (rows.length <= 1) {
        return;
    }

    const row = button.closest(
        '.purchase-item-row'
    );

    if (row) {
        row.remove();
    }

    updatePurchaseTotal();
}


function updatePurchaseTotal() {

    const quantities = document.querySelectorAll(
        'input[name="quantity[]"]'
    );

    const prices = document.querySelectorAll(
        'input[name="cost_price[]"]'
    );

    let total = 0;

    for (let i = 0; i < quantities.length; i++) {

        const quantity =
            parseFloat(quantities[i].value) || 0;

        const price =
            parseFloat(prices[i].value) || 0;

        total += quantity * price;
    }

    const totalElement = document.getElementById(
        'purchase-total'
    );

    if (totalElement) {

        totalElement.textContent =
            'Rs. ' + total.toFixed(2);
    }
}


/* Update total while user types */

document.addEventListener(
    'input',
    function(event) {

        if (
            event.target.name === 'quantity[]' ||
            event.target.name === 'cost_price[]'
        ) {

            updatePurchaseTotal();
        }

    }
);


/* Set initial purchase total */

document.addEventListener(
    'DOMContentLoaded',
    function() {

        updatePurchaseTotal();

    }
);



