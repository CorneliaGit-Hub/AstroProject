// Gérer l'événement de clic sur le bouton "Enregistrer"
document.querySelector("#save-button").addEventListener("click", function () {
    // Récupérer la valeur des champs
    const birthdateVisible = document.querySelector("#birthdate").value; // Champ visible
    const birthdateHidden = document.querySelector("#birthdate-hidden"); // Champ caché

    // Debugging : Afficher les valeurs des champs visibles et cachés
    console.log("Date visible : ", birthdateVisible);
    console.log("Avant mise à jour, champ caché : ", birthdateHidden.value);

    // Vérifier si la date visible est vide ou invalide
    if (!birthdateVisible || birthdateVisible.trim() === "") {
        alert("La date de naissance est vide ou invalide. Veuillez corriger.");
        return;
    }

    // Copier la date visible dans le champ caché
    birthdateHidden.value = birthdateVisible;

    // Debugging : Vérifier la valeur du champ caché après mise à jour
    console.log("Après mise à jour, champ caché : ", birthdateHidden.value);

    // Soumettre le formulaire caché
    document.querySelector("#save-birth-data-form").submit();
});
