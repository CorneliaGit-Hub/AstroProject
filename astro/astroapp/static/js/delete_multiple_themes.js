document.addEventListener("DOMContentLoaded", function () {
    console.log("Gestion de la suppression multiple initialisée.");

    const deleteSelectedButton = document.getElementById("deleteSelected");
    const themeCheckboxes = document.querySelectorAll(".theme-checkbox");

    deleteSelectedButton.addEventListener("click", function () {
        console.log("Bouton 'Supprimer les thèmes sélectionnés' cliqué.");

        // Récupérer les IDs des thèmes sélectionnés
        const selectedIds = Array.from(themeCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.dataset.id);

        console.log("IDs des thèmes sélectionnés :", selectedIds);

        if (selectedIds.length === 0) {
            alert("Aucun thème sélectionné.");
            return;
        }

        // Confirmation
        if (!confirm("Êtes-vous sûr de vouloir supprimer les thèmes sélectionnés ?")) {
            return;
        }

        // Effectuer une requête POST pour supprimer les thèmes
        fetch(`/themes/supprimer_multiple/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ ids: selectedIds })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Réponse JSON reçue :", data);

            if (data.success) {
                alert("Thèmes supprimés avec succès !");
                // Supprime les lignes du tableau
                selectedIds.forEach(id => {
                    const row = document.querySelector(`.theme-checkbox[data-id="${id}"]`).closest("tr");
                    if (row) {
                        row.remove();
                        console.log("Ligne supprimée pour l'ID :", id);
                    }
                });
            } else {
                alert("Erreur lors de la suppression : " + data.message);
            }
        })
        .catch(error => {
            console.error("Erreur réseau :", error);
            alert("Erreur réseau lors de la suppression.");
        });
    });
});
