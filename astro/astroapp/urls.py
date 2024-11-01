from django.urls import path, include
from . import views


urlpatterns = [
    path('birth_data/', views.birth_data, name='birth_data'),  # Vue pour traiter et afficher les données de naissance
    path('planetary_position/', views.planetary_position, name='planetary_position'),  # Vue pour afficher les positions planétaires
    path('enregistrer_theme/', views.enregistrer_theme, name='enregistrer_theme'),
    path('birth_results/', views.display_astrological_wheel, name='birth_results'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
