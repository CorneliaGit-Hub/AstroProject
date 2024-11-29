from django import forms

class BirthDataForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nom")
    birthdate = forms.DateField(label="Date de naissance", widget=forms.DateInput(attrs={'type': 'date'}))
    birthtime = forms.TimeField(label="Heure de naissance", widget=forms.TimeInput(attrs={'type': 'time'}))
    country_of_birth = forms.CharField(max_length=100, label="Pays de naissance")
    city_of_birth = forms.CharField(max_length=100, label="Ville de naissance")
