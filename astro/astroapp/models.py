from django.db import models
from django.conf import settings


class ThemeAstrologique(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="themes")
    nom_du_theme = models.CharField(max_length=255)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    # Ajoutez des champs spécifiques aux calculs astrologiques ici si nécessaire.

    def __str__(self):
        return f"{self.nom_du_theme} - {self.date_de_creation.strftime('%Y-%m-%d')}"
