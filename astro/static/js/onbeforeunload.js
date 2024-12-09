// Vérifier que le script est bien chargé
console.log("Script onbeforeunload.js chargé !");

// Détecter la fermeture ou le rafraîchissement de la page
window.onbeforeunload = function () {
    console.log("onbeforeunload déclenché !");
    console.log("Événement onbeforeunload détecté.");  // Log ajouté ici pour confirmer la détection
    fetch("/delete_image/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    }).then(response => {
        if (response.ok) {
            console.log("Requête de suppression envoyée avec succès !");
        } else {
            console.error("Échec de la suppression de l'image. Code:", response.status);
        }
    }).catch(error => console.error("Erreur réseau :", error));
};
