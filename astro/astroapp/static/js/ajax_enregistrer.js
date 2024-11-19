document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("enregistrer-form");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêche le rechargement de la page
        console.log("Formulaire soumis."); // Débogage : indique que l'événement submit est capturé

        // Récupération du token CSRF
        const csrfToken = form.querySelector("input[name='csrfmiddlewaretoken']").value;
        console.log("Token CSRF récupéré :", csrfToken); // Débogage : vérifie le token CSRF

        // Envoi de la requête AJAX
        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => {
                console.log("Réponse brute reçue :", response); // Débogage : montre la réponse brute
                return response.json();
            })
            .then((data) => {
                console.log("Données JSON reçues :", data); // Débogage : affiche les données JSON

                if (data.success) {
                    // Message de succès
                    messageDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
                    console.log("Message de succès affiché :", data.message); // Débogage : confirme l'affichage du message
                } else {
                    // Message d'erreur
                    messageDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
                    console.log("Message d'erreur affiché :", data.message); // Débogage : confirme l'affichage du message
                }
            })
            .catch((error) => {
                console.error("Erreur AJAX :", error); // Débogage : affiche l'erreur dans la console
                messageDiv.innerHTML = `<p style="color: red;">Une erreur inattendue s'est produite.</p>`;
            });
    });
});
