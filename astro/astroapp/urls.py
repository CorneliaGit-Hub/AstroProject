from django.urls import path, include
from . import views


urlpatterns = [
    path('birth_data/', views.birth_data, name='birth_data'),  # Vue pour traiter et afficher les données de naissance
    path('planetary_position/', views.planetary_position, name='planetary_position'),  # Vue pour afficher les positions planétaires
    path('birth_results/', views.display_astrological_wheel, name='birth_results'),
    path('birth_results/text/', views.birth_results, name='birth_results_text'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('birth_results/enregistrer/', views.enregistrer_naissance, name='enregistrer_naissance'),
    path('themes/', views.liste_themes, name='liste_themes'),
    path('themes/ouvrir/<int:id>/', views.ouvrir_theme, name='ouvrir_theme'),
    path('themes/supprimer/<int:id>/', views.supprimer_theme, name='supprimer_theme'),
    path('themes/supprimer_multiple/', views.supprimer_multiple_themes, name='supprimer_multiple_themes'),
    path('delete_image/', views.delete_image, name='delete_image'),
]
