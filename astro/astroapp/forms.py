from django import forms
from .models import ThemeAstrologique

class BirthDataForm(forms.ModelForm):
    class Meta:
        model = ThemeAstrologique
        fields = ['nom_du_theme']  # Ajoute ici les champs nécessaires pour le formulaire
