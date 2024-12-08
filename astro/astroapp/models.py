from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Ajoute des champs personnalisés si nécessaire
    email = models.EmailField(unique=True)  # Assure l'unicité de l'email

class ThemeAstrologique(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    birthtime = models.TimeField()
    country_of_birth = models.CharField(max_length=255)
    city_of_birth = models.CharField(max_length=255)
    date_de_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.utilisateur.username})"
