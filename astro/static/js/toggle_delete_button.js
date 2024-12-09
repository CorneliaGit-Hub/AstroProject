document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM chargé, gestion de l'affichage du bouton suppression activée.");

    // Récupération des éléments nécessaires
    const deleteButtonContainer = document.getElementById("deleteButtonContainer");
    const themeCheckboxes = document.querySelectorAll(".theme-checkbox");
    const selectAllCheckbox = document.getElementById("selectAll");

    // Fonction pour vérifier si au moins une case est cochée
    function updateDeleteButtonVisibility() {
        const atLeastOneChecked = Array.from(themeCheckboxes).some(checkbox => checkbox.checked);

        // Afficher ou masquer le bouton en fonction des cases cochées
        if (atLeastOneChecked) {
            deleteButtonContainer.style.display = "block";
            console.log("Au moins une case cochée, bouton affiché.");
        } else {
            deleteButtonContainer.style.display = "none";
            console.log("Aucune case cochée, bouton masqué.");
        }
    }

    // Écouteurs sur chaque case individuelle
    themeCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            console.log("Case cochée :", checkbox.checked);
            updateDeleteButtonVisibility();
        });
    });

    // Écouteur sur la case "Tout sélectionner"
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener("change", function () {
            console.log("Case 'Tout sélectionner' changée :", selectAllCheckbox.checked);

            // Coche ou décoche toutes les cases
            themeCheckboxes.forEach(function (checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });

            updateDeleteButtonVisibility();
        });
    }

    // Initialisation : vérifie l'état initial des cases
    updateDeleteButtonVisibility();
});
