from django.urls import path, include
from . import views
from .views import email_sent
from astroapp.views import verifier_connexion




urlpatterns = [
    path('birth_data/', views.birth_data, name='birth_data'),  # Vue pour traiter et afficher les données de naissance
    path('planetary_position/', views.planetary_position, name='planetary_position'),  # Vue pour afficher les positions planétaires
    path('birth_results/', views.display_astrological_wheel, name='birth_results'),
    path('birth_results/text/', views.birth_results, name='birth_results_text'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('verifier-connexion/', verifier_connexion, name='verifier_connexion'),
    path('email-sent/<email>/', email_sent, name='email_sent'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('birth_results/enregistrer/', views.enregistrer_naissance, name='enregistrer_naissance'),
    path('themes/', views.liste_themes, name='liste_themes'),
    path('themes/ouvrir/<int:id>/', views.ouvrir_theme, name='ouvrir_theme'),
    path('themes/supprimer_multiple/', views.supprimer_multiple_themes, name='supprimer_multiple_themes'),
    path('delete_image/', views.delete_image, name='delete_image'),
    path('confirmation/', views.confirm_email, name='confirm_email'),
]
