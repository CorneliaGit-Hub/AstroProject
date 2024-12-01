# Imports standards
import os
import logging  # Ajoute ceci en haut du fichier
logger = logging.getLogger(__name__)  # Initialise le logger
from datetime import datetime
from urllib.parse import urlencode
import json

from .forms import BirthDataForm

# Imports tiers
import pytz
import swisseph as swe
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend sans interface graphique pour Matplotlib
import matplotlib.pyplot as plt  # Import une seule fois
import numpy as np
from matplotlib import font_manager
from matplotlib import patches  # Ajout du module patches pour dessiner les segments

# Imports Django
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now

# Imports internes
from .models import ThemeAstrologique

from astroapp.utils.geolocation_utils import get_birth_location_data
from astroapp.utils.geolocation_utils import geolocate_city
from astroapp.utils.geolocation_utils import determine_timezone
from astroapp.utils.geolocation_utils import extract_date_info

from astroapp.utils.conversions_utils import convert_to_utc
from astroapp.utils.conversions_utils import convert_to_local_and_utc
from astroapp.utils.conversions_utils import create_birth_datetime_and_timestamp
from astroapp.utils.conversions_utils import convert_coordinates_to_dms

from astroapp.utils.data_utils import prepare_theme_data_json
from astroapp.utils.data_utils import prepare_wheel_context
from astroapp.utils.data_utils import prepare_planetary_context
from astroapp.utils.data_utils import extract_request_parameters
from astroapp.utils.data_utils import extract_wheel_data
from astroapp.utils.data_utils import prepare_template_context
from astroapp.utils.data_utils import prepare_aspects_text
from astroapp.utils.data_utils import generate_aspects_and_text

from astroapp.utils.session_data_utils import stocker_donnees_session
from astroapp.utils.session_data_utils import extract_form_data
from astroapp.utils.session_data_utils import extract_birth_data_form

from astroapp.utils.validation_utils import validate_required_fields

from astroapp.calculs.aspects_calculations import calculate_angular_difference
from astroapp.calculs.aspects_calculations import add_aspect_if_present
from astroapp.calculs.aspects_calculations import calculate_aspects
from astroapp.calculs.aspects_calculations import calculate_astrological_aspects

from astroapp.calculs.planet_calculations import calculate_single_planet_position
from astroapp.calculs.planet_calculations import calculate_planet_positions
from astroapp.calculs.planet_calculations import format_planet_positions

from astroapp.calculs.ephemeris_calculations import calculate_julian_day
from astroapp.calculs.ephemeris_calculations import calculate_julian_day_and_planet_positions
from astroapp.calculs.ephemeris_calculations import calculate_julian_and_positions

from astroapp.calculs.houses_calculations import format_house_cusp
from astroapp.calculs.houses_calculations import get_asc_mc
from astroapp.calculs.houses_calculations import calculate_houses
from astroapp.calculs.houses_calculations import calculate_astrological_houses
from astroapp.calculs.houses_calculations import calculate_positions_and_houses

from astroapp.wheel.wheel_symbols import draw_zodiac_symbols
from astroapp.wheel.wheel_symbols import get_planet_colors
from astroapp.wheel.wheel_symbols import display_planet_degrees

from astroapp.wheel.wheel_aspects import get_aspect_style
from astroapp.wheel.wheel_aspects import calculate_aspect_positions
from astroapp.wheel.wheel_aspects import draw_aspects

from astroapp.wheel.wheel_core import create_astrological_figure
from astroapp.wheel.wheel_core import draw_circle
from astroapp.wheel.wheel_core import display_degrees
from astroapp.wheel.wheel_core import generate_astrological_wheel


# ENREGISTRER UN THEME
@login_required
def enregistrer_naissance(request):
    if request.method == "POST":

        # Récupération des données en session
        name = request.session.get("name")
        birthdate = request.session.get("birthdate")
        birthtime = request.session.get("birthtime")
        country_of_birth = request.session.get("country_of_birth")
        city_of_birth = request.session.get("city_of_birth")

        # Vérification que toutes les données sont présentes
        if not all([name, birthdate, birthtime, country_of_birth, city_of_birth]):
            return JsonResponse({
                "success": False,
                "message": "Certaines données nécessaires sont manquantes."
            }, json_dumps_params={'ensure_ascii': False})

        # Enregistrement en base de données
        try:
            ThemeAstrologique.objects.create(
                utilisateur=request.user,
                name=name,
                birthdate=birthdate,
                birthtime=birthtime,
                country_of_birth=country_of_birth,
                city_of_birth=city_of_birth,
            )
            return JsonResponse({
                "success": True,
                "message": "Thème enregistré avec succès !"
            }, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement en base : {str(e)}")
            return JsonResponse({
                "success": False,
                "message": f"Erreur lors de l'enregistrement : {str(e)}"
            }, json_dumps_params={'ensure_ascii': False})

    # Méthode non autorisée
    return JsonResponse({
        "success": False,
        "message": "Méthode non autorisée."
    }, json_dumps_params={'ensure_ascii': False})






# CONNEXION
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('birth_data')  # Redirige vers le formulaire de données de naissance
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('birth_data')  # Redirige vers le formulaire de données de naissance
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('birth_data')  # Redirige vers birth_data après la déconnexion


# THEMES
@login_required
def liste_themes(request):
    if not request.user.is_authenticated:
        return redirect('connexion')  # Redirection si l'utilisateur n'est pas connecté
    
    themes = ThemeAstrologique.objects.filter(utilisateur=request.user).order_by('-id')
    return render(request, 'liste_themes.html', {'themes': themes})

    
@login_required
def ouvrir_theme(request, id):
    # Récupère le thème spécifique pour cet utilisateur
    theme = get_object_or_404(ThemeAstrologique, id=id, utilisateur=request.user)

    # Injecte les données dans la session, en s'assurant que la date est au format ISO
    request.session['name'] = theme.name
    request.session['birthdate'] = theme.birthdate.strftime('%Y-%m-%d')  # Assure le format ISO
    request.session['birthtime'] = theme.birthtime.isoformat()
    request.session['country_of_birth'] = theme.country_of_birth
    request.session['city_of_birth'] = theme.city_of_birth

    # Imprime les valeurs stockées pour vérifier
    print("Session 'name':", request.session['name'])
    print("Session 'birthdate' (ISO format):", request.session['birthdate'])
    print("Session 'birthtime' (ISO format):", request.session['birthtime'])
    print("Session 'country_of_birth':", request.session['country_of_birth'])
    print("Session 'city_of_birth':", request.session['city_of_birth'])

    # Imprime les valeurs des clés pour vérifier leur présence immédiatement après sauvegarde
    print("Session Key-Value pairs after setting in ouvrir_theme:")
    for key, value in request.session.items():
        print(f"{key}: {value}")
        
    # Redirige vers le formulaire principal
    return redirect('birth_data')




@login_required
def supprimer_theme(request, id):
    print(f"Vue supprimer_theme appelée avec ID : {id}")
    try:
        theme = get_object_or_404(ThemeAstrologique, id=id, utilisateur=request.user)

        if request.method == 'POST':
            theme.delete()
            # Réponse JSON pour AJAX
            return JsonResponse({"success": True, "message": "Thème supprimé avec succès !"})
        
        # Si ce n'est pas une requête POST
        return JsonResponse({"success": False, "message": "Requête invalide, POST attendu."}, status=400)

    except Exception as e:
        # En cas d'erreur, retourne un message JSON
        return JsonResponse({"success": False, "message": f"Erreur serveur : {str(e)}"}, status=500)




@login_required
def supprimer_multiple_themes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Récupère les données envoyées dans la requête
            ids = data.get("ids", [])  # Liste des IDs à supprimer

            print(f"IDs reçus pour suppression : {ids}")  # Debugging
            print(f"Utilisateur actuel : {request.user}")  # Debugging

            if not ids:
                return JsonResponse({"success": False, "message": "Aucun ID fourni."})

            # Vérifie et supprime les thèmes appartenant à l'utilisateur
            themes = ThemeAstrologique.objects.filter(id__in=ids, utilisateur=request.user)
            print(f"Thèmes trouvés pour suppression : {[theme.name for theme in themes]}")  # Debugging
            count = themes.count()
            themes.delete()
            print(f"{count} thème(s) supprimé(s).")  # Debugging

            return JsonResponse({"success": True, "message": f"{count} thème(s) supprimé(s) avec succès !"})

        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")  # Debugging
            return JsonResponse({"success": False, "message": f"Erreur : {str(e)}"})

    return JsonResponse({"success": False, "message": "Requête invalide."})








# ZODIAQUE - Fonction pour retourner l'image de la roue zodiacale
def zodiac_wheel(request):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'zodiac_wheel.png')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/png")

# Traite les données de naissance soumises via le formulaire birth_data_form.html, et transmet les résultats astrologiques au template `birth_results.html`.
def birth_data(request):
    # Affiche toutes les données de session pour vérifier leur présence
    print("Session Key-Value pairs on loading birth_data:")
    for key, value in request.session.items():
        print(f"{key}: {value}")
    """
    Gère la soumission des données de naissance via le formulaire.

    - Récupère et valide les données du formulaire `birth_data_form.html`.
    - Calcule les positions planétaires, maisons astrologiques, et aspects.
    - Prépare une roue astrologique visuelle et transmet les données au template `birth_results.html`.

    Paramètres :
    - request (HttpRequest) : Objet représentant la requête HTTP.

    Retour :
    - HttpResponse : Renvoie une page HTML contenant les résultats astrologiques
      ou le formulaire avec un message d'erreur si une étape échoue.
    """
    if request.method == 'POST':

        # Extraire les données du formulaire
        name, birthdate, birthtime, country_of_birth, city_of_birth = extract_birth_data_form(request)

        # Debugging : Afficher les données reçues et celles stockées en session
        print("Date reçue depuis le formulaire :", request.POST.get('birthdate'))
        print("Date de naissance pour l'input :", request.session.get('birthdate'))
        print("Session Data:", request.session.items())

        # Stocker les données en session
        stocker_donnees_session(request, {
            'name': name,
            'birthdate': birthdate,
            'birthtime': birthtime,
            'country_of_birth': country_of_birth,
            'city_of_birth': city_of_birth
        })

        # Valider les champs requis
        fields = [name, birthdate, birthtime, city_of_birth, country_of_birth]
        field_names = ["Nom", "Date de naissance", "Heure de naissance", "Ville de naissance", "Pays de naissance"]
        is_valid, error_message = validate_required_fields(fields, field_names)

        if not is_valid:
            return render(request, 'birth_data_form.html', {'error': error_message})

        # Créer un objet datetime pour la naissance et un timestamp
        birth_datetime, timestamp = create_birth_datetime_and_timestamp(birthdate, birthtime)
        
        # Vérifier si l'année est valide
        birth_year = birth_datetime.year
        if birth_year < 1000 or birth_year > 9999:
            return render(request, 'birth_data_form.html', {
                'error': 'L\'année de naissance doit être comprise entre 1000 et 9999.',
                'name': name,
                'birthdate': birthdate,
                'birthtime': birthtime,
                'country_of_birth': country_of_birth,
                'city_of_birth': city_of_birth
            })

        # Obtenir la géolocalisation et le fuseau horaire
        location, latitude, longitude, timezone_str, error = get_birth_location_data(city_of_birth, country_of_birth)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Convertir les coordonnées en DMS (degrés, minutes, secondes)
        latitude_dms, longitude_dms = convert_coordinates_to_dms(latitude, longitude)

        # Convertir les heures en local et UTC
        birth_datetime_local, birth_datetime_utc, error = convert_to_local_and_utc(birth_datetime, timezone_str)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Calculer le jour julien (JD) et les positions des planètes
        jd, results, planet_positions = calculate_julian_and_positions(birth_datetime_utc)

        # Calculer les maisons astrologiques
        house_results = calculate_astrological_houses(jd, latitude, longitude)

        # Calculer les aspects planétaires et leur texte
        aspects, aspects_text = generate_aspects_and_text(planet_positions)

        # Préparer les données du thème en JSON
        theme_data_json = prepare_theme_data_json(house_results, aspects, planet_positions)

        # Générer la roue astrologique visuelle
        generate_astrological_wheel(planet_positions, house_results, aspects)

        # Préparer le contexte à transmettre au template
        context = prepare_template_context(
            name, results, house_results, aspects, aspects_text,
            birth_datetime_local, birth_datetime_utc, location,
            latitude_dms, longitude_dms, theme_data_json
        )

        return render(request, 'birth_results.html', context)

    # Affichage du formulaire pour une requête GET
    # Vérifier si des données existent dans la session
    print("DEBUG - Date de naissance dans la session (avant extraction) :", request.session.get('birthdate'))

    # Préparer les données initiales pour le formulaire
    initial_data = {
        'name': request.session.get('name', ''),
        'birthdate': request.session.get('birthdate', ''),
        'birthtime': request.session.get('birthtime', ''),
        'country_of_birth': request.session.get('country_of_birth', ''),
        'city_of_birth': request.session.get('city_of_birth', ''),
    }
    print("DEBUG - Données initiales pour le formulaire :", initial_data)

    # Créer un formulaire pré-rempli avec les données initiales
    form = BirthDataForm(initial=initial_data)

    # Supprimer les données de la session après avoir créé le formulaire
    for key in ['name', 'birthdate', 'birthtime', 'country_of_birth', 'city_of_birth']:
        if key in request.session:
            del request.session[key]

    # Vérification finale de la session
    print("DEBUG - Session après suppression des clés :", dict(request.session.items()))

    # Rendre la page avec le formulaire
    return render(request, 'birth_data_form.html', {
        'form': form,
        'birthdate_debug': initial_data.get('birthdate', '')  # Passer directement les données initiales
    })



# Convertit un objet datetime en UTC en appliquant le fuseau horaire spécifié.
def convert_to_utc(date_obj, timezone_str):
    """Convertit un objet datetime en UTC selon le fuseau horaire fourni."""
    try:
        # Applique le fuseau horaire local fourni pour convertir la date en UTC
        local_tz = pytz.timezone(timezone_str)
        
        # Si l'objet date n'a pas encore de fuseau horaire, applique local_tz
        if date_obj.tzinfo is None:
            date_obj = local_tz.localize(date_obj)
        
        # Conversion en UTC
        date_utc = date_obj.astimezone(pytz.utc)
        
        return date_utc, None

    except Exception as e:
        error_message = f"Erreur de conversion du fuseau horaire : {e}"
        return None, error_message


# Calcule les positions planétaires et les maisons, puis transmet les données au template `planetary_position.html` pour affichage.
def planetary_position(request):# Calculer le jour julien (JD)
    """
    Calcule les positions planétaires et les maisons astrologiques pour une date et un lieu donnés.

    - Extrait les paramètres nécessaires depuis la requête HTTP.
    - Récupère les informations géographiques et temporelles.
    - Calcule les positions des planètes et des maisons astrologiques.
    - Transmet les données calculées au template `planetary_position.html`.

    Paramètres :
    - request (HttpRequest) : Objet représentant la requête HTTP.

    Retour :
    - HttpResponse : Renvoie une page HTML contenant les positions planétaires
      ou un message d'erreur si une étape échoue.
    """

    # Appel de la foction : def extract_request_parameters
    selected_date, city_of_birth, country_of_birth = extract_request_parameters(request)

    # Vérifier si les champs requis sont fournis
    # Valider les champs requis
    fields = [selected_date, city_of_birth, country_of_birth]
    field_names = ["Date de naissance", "Ville de naissance", "Pays de naissance"]
    is_valid, error_message = validate_required_fields(fields, field_names)

    if not is_valid:
        return HttpResponse(error_message)

    

    # Appel de la fonction pour extraire les informations de date : def extract_date_info
    date_obj, local_day_str, local_month_str, local_year_str = extract_date_info(selected_date)

    # Utiliser le geolocator pour obtenir la latitude et la longitude    print("Debug - Tentative de géolocalisation avec geolocator")
    latitude, longitude, error = geolocate_city(city_of_birth, country_of_birth)
    if error:
        logger.error(f"Erreur dans planetary_position : {error}")
        return HttpResponse(error)


    # Debugging: Afficher les valeurs de latitude et longitude
    logger.debug(f"Latitude: {latitude}, Longitude: {longitude}")
    logger.debug(f"Ville de naissance: {city_of_birth}, Pays de naissance: {country_of_birth}")



    # Appel à la fonction pour Fixer manuellement le fuseau horaire si le lieu est Cayenne : def determine_timezone
    timezone_at, error = determine_timezone(city_of_birth, country_of_birth, latitude, longitude)
    if error:
        return HttpResponse(error)
    # Appel à la fonction
    date_utc, error = convert_to_utc(date_obj, timezone_at)
    if error:
        return HttpResponse(error)

    # Appel de la fonction pour calculer le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(date_utc)

    # Appel de la fonction pour calculer les positions planétaireset les maisons : 
    results, planet_positions, house_results = calculate_positions_and_houses(jd, latitude, longitude)

    # Appel de la fonction pour préparer le contexte : def prepare_planetary_context
    context = prepare_planetary_context(
        selected_date, city_of_birth, country_of_birth,
        local_day_str, local_month_str, local_year_str,
        results, house_results
    )
    return render(request, 'planetary_position.html', context)
    


# Génère et transmet les données nécessaires pour afficher la roue astrologique dans le template `birth_results.html`.
def display_astrological_wheel(request):
    # Appel de la fonciton pour Charger les données depuis les paramètres GET : def extract_wheel_data
    house_results, aspects, planet_positions = extract_wheel_data(request)

    # Appel de la fonciotn pour Formater les aspects en texte lisible : def prepare_aspects_text
    aspects_text = prepare_aspects_text(aspects, planet_positions)


    # Appel de la fonction pour préparer le contexte pour le rendu et passer les données formatées au template : def prepare_wheel_contex
    context = prepare_wheel_context(planet_positions, house_results, aspects_text)
    return render(request, 'birth_results.html', context)


# Prépare et transmet les données astrologiques au template `birth_results.html` pour l'affichage.
def birth_results(request):
    # Récupération simplifiée des données de thème
    house_results = {}
    aspects = []
    planet_positions = {}

    # Rendre les données au template
    return render(request, 'birth_results.html', {
        'house_results': house_results,
        'aspects': aspects,
        'planet_positions': planet_positions,
    })

