document.addEventListener("DOMContentLoaded", function () {
    console.log("panel-director.js loaded");
    const navLinks = document.querySelectorAll(".nav-links .nav-item a");
    const sections = document.querySelectorAll("#mainContent > div");

    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetSection = this.getAttribute("href").substring(1);

            sections.forEach((section) => {
                if (section.id === targetSection) {
                    section.style.display = "block";
                } else {
                    section.style.display = "none";
                }
            });
        });
    });
});