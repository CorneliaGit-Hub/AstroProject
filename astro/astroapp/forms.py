from django import forms

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
