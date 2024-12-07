from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BirthDataForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'value': '%Y-%m-%d'}),
        input_formats=['%Y-%m-%d'],  # Assure l'acceptation du format ISO
        required=True
    )
    birthtime = forms.TimeField(required=True)
    country_of_birth = forms.CharField(max_length=100, required=True)
    city_of_birth = forms.CharField(max_length=100, required=True)

class CustomUserCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=150, required=True, label="Nom")
    prenom = forms.CharField(max_length=150, required=True, label="Prénom")

    class Meta:
        model = User
        fields = ['username', 'nom', 'prenom', 'password1', 'password2']
