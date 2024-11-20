document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("enregistrer-form");
    const button = document.getElementById("enregistrer");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêche le rechargement de la page

        // Changer le texte du bouton pour indiquer l'état
        button.innerText = "Enregistrement en cours...";
        button.disabled = true;

        // Jouer un son de clic
        const audio = new Audio('/static/sounds/registered.wav');
        audio.play();

        // Envoi de la requête AJAX
        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": form.querySelector("input[name='csrfmiddlewaretoken']").value,
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    button.innerText = "Enregistré avec succès !";
                    messageDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
                } else {
                    button.innerText = "Erreur lors de l'enregistrement";
                    messageDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
                }
            })
            .catch((error) => {
                console.error("Erreur AJAX :", error);
                button.innerText = "Erreur inattendue";
                messageDiv.innerHTML = `<p style="color: red;">Une erreur s'est produite.</p>`;
            })
            .finally(() => {
                // Réinitialiser le bouton après un délai
                setTimeout(() => {
                    button.innerText = "Enregistrer";
                    button.disabled = false;
                }, 3000);
            });
    });
});
