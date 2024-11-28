document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("enregistrer-form");
    const button = document.getElementById("enregistrer");
    const spinner = document.getElementById("spinner");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêche le rechargement de la page

        // Affiche le spinner et désactive le bouton
        spinner.style.display = "block";
        button.innerText = "Enregistrement en cours...";
        button.disabled = true;

        // Récupération du token CSRF
        const csrfToken = form.querySelector("input[name='csrfmiddlewaretoken']").value;

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => {
                // Vérifie si la réponse est une redirection
                if (response.redirected) {
                    console.log("Redirection détectée vers :", response.url);
                    window.location.href = response.url;
                    return;
                }

                // Vérifie le statut HTTP
                if (!response.ok) {
                    console.warn("Statut HTTP inattendu :", response.status);
                    throw new Error("Erreur HTTP détectée");
                }

                // Si pas de redirection, renvoie le JSON
                return response.json();
            })
            .then((data) => {
                if (data && data.success) {
                    console.log("Enregistrement réussi :", data.message);

                    // Jouer le son en cas de succès
                    const audio = new Audio('/static/sounds/registered.wav');
                    audio.play().then(() => {
                        console.log("Son joué avec succès.");
                    }).catch((error) => {
                        console.error("Erreur lors de la lecture du son :", error);
                    });

                    // Affiche le message de succès
                    button.innerText = "Enregistré avec succès !";
                    button.classList.add("registered");
                    messageDiv.innerHTML = `<p style="color: #A9CE02; font-weight:bold">${data.message}</p>`;
                } else if (data && data.redirect_url) {
                    console.log("Redirection requise vers :", data.redirect_url);
                    window.location.href = data.redirect_url;
                } else {
                    console.error("Erreur lors de l'enregistrement :", data.message);
                    afficherMessageErreur("Une erreur s'est produite. Êtes-vous connecté ?");
                }
            })
            .catch((error) => {
                console.error("Erreur lors de la requête AJAX :", error);
                if (error.message === "Erreur HTTP détectée") {
                    console.warn("Aucune action requise pour les redirections.");
                } else {
                    afficherMessageErreur("Une erreur s'est produite. Êtes-vous connecté ?");
                }
            })
            .finally(() => {
                setTimeout(() => {
                    spinner.style.display = "none"; // Cache le spinner après un délai
                    button.disabled = false; // Réactive le bouton
                }, 1000); // Délai de 1 seconde
            });
    });

    // Fonction pour afficher le message d'erreur avec un délai
    function afficherMessageErreur(message) {
        setTimeout(() => {
            messageDiv.innerHTML = `<p style="color: #F9074C; font-weight: bold;">${message}</p>`;
            button.innerText = "Erreur inattendue";
        }, 500); // Retard d’affichage de 500ms
    }

    // Test pour la lecture audio
    console.log("Test de lecture du son...");
    const testAudio = new Audio('/static/sounds/registered.wav');
    testAudio.play()
        .then(() => console.log("Son joué avec succès."))
        .catch((error) => console.error("Erreur lors de la lecture du son :", error));
});
