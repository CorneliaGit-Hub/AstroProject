// Attendre que le DOM soit prêt
document.addEventListener("DOMContentLoaded", function () {
    // Bouton pour remonter en haut
    const scrollUpButton = document.querySelector(".scroll-up");
    // Bouton pour descendre en bas
    const scrollDownButton = document.querySelector(".scroll-down");

    // Scroll vers le haut
    scrollUpButton.addEventListener("click", function (e) {
        e.preventDefault(); // Empêche le comportement par défaut
        window.scrollTo({
            top: 0,
            behavior: "smooth", // Animation fluide
        });
    });

    // Scroll vers le bas
    scrollDownButton.addEventListener("click", function (e) {
        e.preventDefault(); // Empêche le comportement par défaut
        window.scrollTo({
            top: document.body.scrollHeight, // Descend jusqu'à la fin de la page
            behavior: "smooth", // Animation fluide
        });
    });
});
