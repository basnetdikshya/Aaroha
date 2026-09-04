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