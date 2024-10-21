from django.urls import path
from . import views

urlpatterns = [
    path('birth-data/', views.birth_data, name='birth_data'),  # URL pour le formulaire de données de naissance
    path('planetary-position/', views.planetary_position, name='planetary_position'),  # URL pour les positions planétaires
    path('zodiac-wheel/', views.wheel_view, name='zodiac_wheel'),  # URL pour afficher la roue astrologique
]
