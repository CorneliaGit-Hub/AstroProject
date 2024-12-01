document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM chargé, initialisation du script.");

    // Récupère les éléments nécessaires
    let deleteModal = document.getElementById("deleteModal");
    console.log("Fenêtre modale trouvée :", deleteModal);

    let confirmDeleteButton = document.getElementById("confirmDelete");
    console.log("Bouton 'Confirmer' trouvé :", confirmDeleteButton);

    let cancelDeleteButton = document.getElementById("cancelDelete");
    console.log("Bouton 'Annuler' trouvé :", cancelDeleteButton);

    let currentThemeId = null;

    // Récupérer le token CSRF
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log("Token CSRF récupéré :", csrfToken);

    // Cible tous les boutons "Supprimer"
    document.querySelectorAll(".delete-btn").forEach(function (deleteButton) {
        console.log("Bouton 'Supprimer' détecté :", deleteButton);
        deleteButton.addEventListener("click", function (event) {
            event.preventDefault(); // Empêche toute redirection
            currentThemeId = this.getAttribute("data-id"); // Récupère l'ID depuis data-id
            console.log("Bouton 'Supprimer' cliqué pour l'ID :", currentThemeId);
            deleteModal.style.display = "block"; // Affiche la modale
            document.getElementById("modalOverlay").style.display = "block"; // Affiche l'arrière-plan
        });
    });

    // Bouton "Confirmer"
    confirmDeleteButton.addEventListener("click", function () {
        console.log("Bouton 'Confirmer' cliqué pour l'ID :", currentThemeId);

        if (currentThemeId) {
            console.log("currentThemeId avant la suppression :", currentThemeId);

            fetch(`/themes/supprimer/${currentThemeId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            })
                .then(response => {
                    console.log("Réponse brute reçue :", response);
                    return response.json();
                })
                .then(data => {
                    console.log("Données JSON reçues :", data);
                    if (data.success) {
                        console.log("Thème supprimé avec succès !");
                        // Supprime la ligne du tableau sans recharger la page
                        const row = document.querySelector(`a[data-id='${currentThemeId}']`).closest("tr");
                        if (row) {
                            row.remove();
                            console.log("Ligne supprimée du tableau :", row);
                        } else {
                            console.error("Ligne non trouvée pour l'ID :", currentThemeId);
                        }
                    } else {
                        alert("Erreur : " + data.message);
                        console.error("Erreur de suppression côté serveur :", data.message);
                    }
                    deleteModal.style.display = "none"; // Ferme la modale
                    document.getElementById("modalOverlay").style.display = "none"; // Ferme l'arrière-plan
                })
                .catch(error => {
                    alert("Erreur réseau : " + error);
                    console.error("Erreur réseau :", error);
                    deleteModal.style.display = "none"; // Ferme la modale
                    document.getElementById("modalOverlay").style.display = "none"; // Ferme l'arrière-plan
                });
        } else {
            alert("Aucun ID de thème trouvé.");
            console.error("Aucun ID trouvé lors de la tentative de suppression.");
        }
    });

    // Bouton "Annuler"
    cancelDeleteButton.addEventListener("click", function () {
        console.log("Bouton 'Annuler' cliqué. Fermeture de la modale.");
        deleteModal.style.display = "none"; // Ferme la modale
        document.getElementById("modalOverlay").style.display = "none"; // Ferme l'arrière-plan
    });
});
