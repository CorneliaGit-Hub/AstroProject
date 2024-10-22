from django.urls import path
from . import views

urlpatterns = [
    path('birth_data/', views.birth_data, name='birth_data'),  # Vue pour traiter et afficher les données de naissance
    path('planetary_position/', views.planetary_position, name='planetary_position'),  # Vue pour afficher les positions planétaires
]
