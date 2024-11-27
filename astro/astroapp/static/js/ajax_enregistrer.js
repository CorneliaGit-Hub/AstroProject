document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("enregistrer-form");
    const button = document.getElementById("enregistrer");
    const spinner = document.getElementById("spinner");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Empêche le rechargement de la page

        // Affiche le spinner
        spinner.style.display = "block";

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
		
			.then((response) => {
				if (response.redirected) {
					window.location.href = response.url; // Redirige vers l'URL reçue
				} else {
					return response.json();
				}
			})
			
			.then((data) => {
				if (data.success) {
					button.innerText = "Enregistré avec succès !";
					button.classList.add("registered");
					button.disabled = true;
					messageDiv.innerHTML = `<p style="color: #A9CE02; font-weight:bold">${data.message}</p>`;
				} else {
					if (data.redirect_url) {
						window.location.href = data.redirect_url; // Redirige vers l'URL spécifiée
					} else {
						button.innerText = "Erreur lors de l'enregistrement";
						messageDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
					}
				}
			})




			.catch((error) => {
				if (error.response && error.response.status === 403) {
					window.location.href = "/connexion/"; // Redirection vers la page de connexion
				} else {
					console.error("Erreur AJAX :", error);
					button.innerText = "Erreur inattendue";
					messageDiv.innerHTML = `<p style="color: red;">Une erreur s'est produite.</p>`;
				}
			})

			.finally(() => {
				setTimeout(() => {
					spinner.style.display = "none"; // Cacher le spinner après un délai
				}, 1000); // Délai de 2 secondes
			});
    });
});
