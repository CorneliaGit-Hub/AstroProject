Documentation des Variables
Fichier : extract_variables.py
file_path : chemin d'accès au fichier analysé.
project_directory : répertoire principal du projet à analyser.
variables : liste des variables extraites d’un fichier.
all_variables : dictionnaire contenant toutes les variables par fichier.
tree : arbre syntaxique abstrait (AST) du fichier en cours d’analyse.
variables_dict : dictionnaire central des variables pour l’analyse.
Fichier : manage.py
Pas de variables spécifiques à documenter ici.
Fichier : astroapp/admin.py
Pas de variables spécifiques à documenter ici.
Fichier : astroapp/apps.py
Pas de variables spécifiques à documenter ici.
Fichier : astroapp/forms.py
Pas de variables spécifiques à documenter ici.
Fichier : astroapp/models.py
date_de_creation : date de création d’un enregistrement.
utilisateur : référence à l’utilisateur associé.
nom_du_theme : nom du thème astrologique.
Fichier : astroapp/urls.py
urlpatterns : liste des URL gérées par l’application.
Fichier : astroapp/views.py
1. Coordonnées et Données de Naissance
latitude, longitude : coordonnées de naissance.
birth_datetime, birth_datetime_local, birth_datetime_utc : date et heure de naissance sous différents formats.
birthdate, birthtime : date et heure de naissance simplifiées.
country_of_birth, city_of_birth : informations de lieu de naissance.
timezone_at, timezone_str, local_tz : fuseau horaire de naissance.
2. Données Astrologiques
planet1, planet2 : noms ou identifiants de planètes.
degrees, sign_degree : degrés associés aux positions astrologiques.
aspects, aspect_styles, aspect_orbs : aspects entre planètes.
elements, element : éléments astrologiques (feu, eau, air, terre).
signs, sign_index : liste des signes et leur indice.
asc, asc_angle, asc_mc_houses : angle et position de l’ascendant.
mc : milieu du ciel (Medium Coeli).
3. Affichage et Mise en Forme
x_inner, x_outer, y_inner, y_outer, x_text, y_text : positions X et Y pour affichage.
triangle, circle, center_circle, outer_border_circle : éléments graphiques.
degree_start, degree_mid, degree_end : délimitation des degrés pour les segments.
angle_mid, angle_mid_corrected, angle_corrected : ajustements d’angles pour affichage.
facecolor, symbol_color, sign_colors : couleurs de fond et des signes.
4. Données JSON et Thèmes
theme_data_json, theme_data : données JSON du thème astrologique.
house_results_str, house_results : résultats calculés pour les maisons.
url, form : URL d’accès et formulaire de saisie.
5. Symboles et Styles
zodiac_symbols, planet_symbols : symboles des signes du zodiaque et des planètes.
symbol, symbol_size : symbole astrologique et sa taille.
roman_numerals, roman_house_num : chiffres romains pour les maisons.
prop, style : styles et propriétés pour affichage.
6. Fonctions Utilitaires
timestamp : marqueur de temps.
geolocator : objet pour la géolocalisation.
image_path : chemin de sauvegarde de l’image de la roue astrologique.
Fichier : astroapp/migrations/0001_initial.py
dependencies : dépendances pour la migration.
initial : booléen indiquant si la migration est initiale.
operations : opérations associées à la migration.
Fichier : astroapp/templatetags/custom_filters.py
seconds, minutes : données temporelles.
register : registre des filtres personnalisés.
degrees : degrés utilisés dans les filtres.
Fichier : astroconfig/asgi.py
Pas de variables spécifiques à documenter ici.
Fichier : astroconfig/settings.py
INSTALLED_APPS : liste des applications installées.
AUTH_PASSWORD_VALIDATORS : validateurs de mot de passe.
STATIC_URL, STATIC_ROOT, STATICFILES_DIRS : chemins pour les fichiers statiques.
ROOT_URLCONF : configuration des URL racine.
SECRET_KEY : clé secrète de Django.
USE_TZ : option d’utilisation des fuseaux horaires.
TEMPLATES : configuration des templates.
BASE_DIR : répertoire de base du projet.
LANGUAGE_CODE : langue par défaut du projet.
MIDDLEWARE : liste des middlewares activés.
DEBUG : option de mode de développement.
TIME_ZONE : fuseau horaire par défaut.
ALLOWED_HOSTS : liste des hôtes autorisés.
DEFAULT_AUTO_FIELD : champ par défaut pour les modèles.
USE_I18N : option d’internationalisation.
DATABASES : configuration de la base de données.
WSGI_APPLICATION : application WSGI.
Fichier : astroconfig/urls.py
urlpatterns : liste des URL pour la configuration.
Fichier : astroconfig/wsgi.py
application : application WSGI.