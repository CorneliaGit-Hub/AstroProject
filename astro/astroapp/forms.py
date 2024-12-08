from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assure-toi d'importer CustomUser

class CustomUserCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=150, required=True, label="Nom")
    prenom = forms.CharField(max_length=150, required=True, label="Prénom")
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'prenom', 'nom', 'password1', 'password2']

class BirthDataForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Assure l'acceptation du format ISO
        required=True
    )
    birthtime = forms.TimeField(required=True)
    country_of_birth = forms.CharField(max_length=100, required=True)
    city_of_birth = forms.CharField(max_length=100, required=True)
