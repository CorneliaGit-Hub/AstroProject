document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM chargé, initialisation du script de suppression multiple.");

    const deleteButton = document.getElementById("deleteSelected");
    const themeCheckboxes = document.querySelectorAll(".theme-checkbox");

    if (!deleteButton || themeCheckboxes.length === 0) {
        console.error("Bouton de suppression ou cases à cocher non trouvés !");
        return;
    }

    deleteButton.addEventListener("click", function () {
        console.log("Bouton 'Supprimer les thèmes sélectionnés' cliqué.");

        // Récupère les IDs des cases cochées
        const selectedIds = Array.from(themeCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.dataset.id);

        const uniqueIds = [...new Set(selectedIds)]; // Supprime les doublons
        console.log("IDs uniques sélectionnés :", uniqueIds);

        if (uniqueIds.length === 0) {
            alert("Aucun thème sélectionné !");
            return;
        }

        // Envoie la requête au serveur
        fetch("/themes/supprimer_multiple/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ ids: uniqueIds }),
        })
            .then(response => {
                console.log("Réponse brute du serveur :", response);
                if (!response.ok) {
                    throw new Error("Erreur réseau !");
                }
                return response.json();
            })
            .then(data => {
                console.log("Réponse JSON du serveur :", data);
                if (data.success) {
                    alert(data.message);
                    // Supprime les lignes du tableau sans recharger la page
                    uniqueIds.forEach(id => {
                        const row = document.querySelector(`.theme-checkbox[data-id='${id}']`).closest("tr");
                        if (row) {
                            row.remove();
                            console.log(`Ligne avec ID ${id} supprimée.`);
                        }
                    });
                } else {
                    alert("Erreur : " + data.message);
                }
            })
            .catch(error => {
                console.error("Erreur lors de la requête :", error);
                alert("Erreur réseau lors de la suppression.");
            });
    });
});
