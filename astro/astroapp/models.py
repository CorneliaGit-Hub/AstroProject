from django.db import models
from django.contrib.auth.models import User

class ThemeAstrologique(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    nom_du_theme = models.CharField(max_length=255)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_naissance = models.DateField(default='2000-01-01')  # Valeur par défaut ajoutée
    heure_naissance = models.TimeField(default='00:00:00')  # Valeur par défaut ajoutée
    pays = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom_du_theme} ({self.utilisateur.username})"

