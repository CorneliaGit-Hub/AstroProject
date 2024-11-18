document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#save-birth-data-form");

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Empêche le rechargement de la page

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Erreur lors de l'enregistrement.");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        alert("Données enregistrées avec succès !");
                    } else {
                        alert("Une erreur est survenue : " + data.error);
                    }
                })
                .catch((error) => {
                    console.error("Erreur AJAX : ", error);
                    alert("Erreur lors de l'enregistrement.");
                });
        });
    }
});
