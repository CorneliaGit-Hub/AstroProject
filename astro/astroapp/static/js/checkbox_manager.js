document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM chargé, gestion des cases à cocher activée.");

    const selectAllCheckbox = document.getElementById("selectAll");
    const themeCheckboxes = document.querySelectorAll(".theme-checkbox");

    // Gère la sélection/désélection de toutes les cases
    selectAllCheckbox.addEventListener("change", function () {
        console.log("Case 'Tout sélectionner' changée :", this.checked);
        themeCheckboxes.forEach(function (checkbox) {
            checkbox.checked = selectAllCheckbox.checked;
            console.log(`Case ${checkbox.dataset.id} :`, checkbox.checked);
        });
    });

    // Gère la mise à jour de la case "Tout sélectionner" quand une case individuelle change
    themeCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const allChecked = Array.from(themeCheckboxes).every(cb => cb.checked);
            const noneChecked = Array.from(themeCheckboxes).every(cb => !cb.checked);

            selectAllCheckbox.indeterminate = !allChecked && !noneChecked;
            selectAllCheckbox.checked = allChecked;
            console.log("Mise à jour de 'Tout sélectionner' :", selectAllCheckbox.checked);
        });
    });
});
