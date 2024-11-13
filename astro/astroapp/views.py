import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import swisseph as swe
from zoneinfo import ZoneInfo
from django.http import HttpResponse
from django.conf import settings
import os
import time
import matplotlib
matplotlib.use('Agg')  # Utiliser le backend sans interface graphique pour Matplotlib
import matplotlib.pyplot as plt  # Import une seule fois
import numpy as np
from matplotlib import font_manager
from matplotlib import patches  # Ajout du module patches pour dessiner les segments
import matplotlib.patches as patches
from django.utils.timezone import now
timestamp = int(now().timestamp())
from django.shortcuts import render, redirect
from .models import ThemeAstrologique
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
import json
from django.utils.http import urlencode

# ENREGISTRER UN THEME
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



# ZODIAQUE
# Fonction pour retourner l'image de la roue zodiacale
def zodiac_wheel(request):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'zodiac_wheel.png')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/png")

# 1- Fonction pour obtenir le signe astrologique à partir d'un degré
def get_zodiac_sign(degree):
    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
    ]
    sign_index = int(degree // 30)
    sign_degree = degree % 30
    return signs[sign_index], sign_degree





# PLANETES 
def calculate_single_planet_position(jd, planet_id):
    """Calcule la position d'une planète en fonction du jour julien."""
    position, _ = swe.calc_ut(jd, planet_id)
    degree = position[0]
    sign, sign_degree = get_zodiac_sign(degree)

    # Afficher la position pour débogage
    print(f"Débogage : Planète ID {planet_id} - Degré :", degree, ", Signe :", sign, ", Degré dans le signe :", sign_degree)

    planet_data = {
        'degree': degree,
        'sign': sign,
        'sign_degree': sign_degree,
    }
    return planet_data, degree


def calculate_single_planet_position(jd, planet_id):
    """Calcule la position d'une planète en fonction du jour julien."""
    position, _ = swe.calc_ut(jd, planet_id)
    degree = position[0]
    sign, sign_degree = get_zodiac_sign(degree)

    # Afficher la position pour débogage
    print(f"Débogage : Planète ID {planet_id} - Degré :", degree, ", Signe :", sign, ", Degré dans le signe :", sign_degree)

    planet_data = {
        'degree': degree,
        'sign': sign,
        'sign_degree': sign_degree,
    }
    return planet_data, degree


def format_planet_positions(results, planet_positions):
    """Prépare les résultats des positions planétaires pour le retour."""
    # Affiche les résultats pour vérification
    print("Débogage : Résultats des positions des planètes ->", results)
    print("Débogage : Positions des planètes en liste ->", planet_positions)
    return results, planet_positions


# 2- Fonction pour calculer les positions des planètes
def calculate_planet_positions(jd):
    planets = {
        'Soleil': swe.SUN,
        'Lune': swe.MOON,
        'Mercure': swe.MERCURY,
        'Vénus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturne': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluton': swe.PLUTO,
    }
    results = {}
    planet_positions = []

    print("Débogage : Calcul des positions des planètes pour le jour julien (JD) ->", jd)


    for planet_name, planet_id in planets.items():
        # Appel de la fonction pour calculer la position d'une planète : def calculate_single_planet_position
        planet_data, planet_degree = calculate_single_planet_position(jd, planet_id)
        results[planet_name] = planet_data
        planet_positions.append((planet_name, planet_degree))


    # Appel de la fonction pour formater les résultats avant de les renvoyer : def format_planet_positions(
    return format_planet_positions(results, planet_positions)
    

# 2-Fonction pour convertir les degrés en degrés, minutes et secondes
def convert_to_dms(degree):
    degrees = int(degree)
    minutes = int((degree - degrees) * 60)
    seconds = round(((degree - degrees) * 60 - minutes) * 60, 2)
    return degrees, minutes, seconds






# MAISONS
def format_house_cusp(cusp):
    """Formate les données de la cuspide d'une maison en fonction de son degré."""
    sign, sign_degree = get_zodiac_sign(cusp)
    degrees, minutes, seconds = convert_to_dms(cusp)
    return {
        'degree': cusp,
        'sign': sign,
        'sign_degree': sign_degree,
        'degree_dms': f"{degrees}°{minutes}'{seconds}''"
    }


def get_asc_mc(ascmc):
    """Récupère les positions de l'Ascendant (ASC) et du Milieu du Ciel (MC) depuis les données ascmc."""
    asc = ascmc[0]
    mc = ascmc[1]
    return asc, mc


# 3- Fonction pour calculer les maisons astrologiques avec les degrés totaux et DMS
def calculate_houses(jd, latitude, longitude):
    # Utiliser les mêmes fonctions de calcul que dans zodiacwheel.py
    house_cuspids, ascmc = swe.houses(jd, latitude, longitude, b'P')
    
    # Formater les résultats comme dans zodiacwheel.py
    house_results = {}
    for i, cusp in enumerate(house_cuspids):
        # Appel de la fonction pour formater les données de la maison
        house_results[f'Maison {i + 1}'] = format_house_cusp(cusp)


    # Appel de la fonction pour obtenir l'ASC et le MC : def get_asc_mc(ascmc)
    asc, mc = get_asc_mc(ascmc)

    return house_results    





# GEOLOCALISATION
# Fonction pour obtenir la géolocalisation d'un lieu
def get_location(city, country):
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city}, {country}", timeout=10)
    
    if not location:
        return None, "Lieu de naissance introuvable."
    # Ajoute ce print ici
    print("Géolocalisation - Latitude :", location.latitude, "Longitude :", location.longitude)
    return location, None  # Retourne la localisation et None pour indiquer qu'il n'y a pas d'erreur

# Fonction pour obtenir le fuseau horaire d'une localisation
def get_timezone(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    
    if not timezone_str:
        return None, "Fuseau horaire non trouvé."
    
    return timezone_str, None  # Retourne le fuseau horaire et None pour indiquer qu'il n'y a pas d'erreur


def localize_datetime(birth_datetime, timezone_str):
    """Gère la localisation de birth_datetime en tenant compte du fuseau horaire spécifique."""
    if timezone_str == "America/Cayenne":
        timezone = pytz.timezone("Etc/GMT+3")
        return timezone.localize(birth_datetime)
    else:
        return birth_datetime.replace(tzinfo=ZoneInfo(timezone_str))


def convert_to_utc(local_datetime):
    """Convertit un datetime localisé en heure UTC."""
    return local_datetime.astimezone(ZoneInfo("UTC"))


# Fonction pour convertir une date de naissance en heures locales et UTC
def convert_birth_datetime(birth_datetime, timezone_str):
    try:
        # Appel de la fonction pour convertir en heure locale :  def localize_datetime
        birth_datetime_local = localize_datetime(birth_datetime, timezone_str)
        
        # Appel de la fonction pour convertir l'heure locale en UTC : def convert_to_utc
        birth_datetime_utc, error = convert_to_utc(birth_datetime_local, timezone_str)  # Ajoute timezone_str

        # Si une erreur est détectée, retourne l'erreur
        if error:
            return None, None, error
            
        # Ajoute ces prints ici
        print("Fuseau Horaire :", timezone_str)
        print("Date/Heure UTC :", birth_datetime_utc)
    
        # Retourne les dates locales et UTC sans erreur
        return birth_datetime_local, birth_datetime_utc, None

    except Exception as e:
        # En cas d'erreur, retourne None et le message d'erreur
        return None, None, f'Erreur de conversion : {e}'


# julian_day
def calculate_julian_day(birth_datetime_utc):
    """Calcule le jour julien (JD) à partir d'une date UTC."""
    return swe.julday(
        birth_datetime_utc.year,
        birth_datetime_utc.month,
        birth_datetime_utc.day,
        birth_datetime_utc.hour + birth_datetime_utc.minute / 60.0
    )

def calculate_julian_day_and_planet_positions(birth_datetime_utc, latitude, longitude):

    # Appel de la fonction pour calculer le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(birth_datetime_utc)

    
    # Calcul des positions des planètes
    results, planet_positions = calculate_planet_positions(jd)

    # Ajoute ce print ici
    print("Jour Julien Calculé :", jd)
    return jd, results, planet_positions


# Fonction pour calculer les maisons astrologiques
def calculate_astrological_houses(jd, latitude, longitude):
    # Utiliser les mêmes fonctions de calcul que dans zodiacwheel.py
    house_results = calculate_houses(jd, latitude, longitude)
    
    return house_results



# ASPECTS
# Fonction pour calculer les aspects planétaires
def calculate_astrological_aspects(planet_positions):
    aspects = calculate_aspects(planet_positions)
    return aspects


def add_aspect_if_present(aspects, planet1, pos1, planet2, pos2, diff, aspect_definitions, aspect_orbs):
    """Vérifie si un aspect existe entre deux positions planétaires et l'ajoute à la liste des aspects."""
    for aspect_name, aspect_angle in aspect_definitions.items():
        orbe = aspect_orbs[aspect_name]
        if abs(diff - aspect_angle) <= orbe:
            aspects.append((aspect_name, pos1, pos2))


def calculate_angular_difference(pos1, pos2):
    """Calcule la différence angulaire minimale entre deux positions planétaires."""
    diff = abs(pos1 - pos2)
    return min(diff, 360 - diff)


# Fonction pour afficher les aspects planétaires
def calculate_aspects(planet_positions):
    aspects = []
    aspect_definitions = {
        'Conjonction': 0,
        'Sextile': 60,
        'Carré': 90,
        'Trigone': 120,
        'Opposition': 180,
    }
    aspect_orbs = {
        'Conjonction': 8,
        'Sextile': 6,
        'Carré': 6,
        'Trigone': 8,
        'Opposition': 8,
    }

    for i in range(len(planet_positions)):
        for j in range(i + 1, len(planet_positions)):
            planet1, pos1 = planet_positions[i]
            planet2, pos2 = planet_positions[j]
            
            # Appel la fonction qui Calcule la différence angulaire minimale entre deux positions
            diff = calculate_angular_difference(pos1, pos2)


            # Appel la focntion qui Vérifie si un aspect est présent et l'ajoute s'il est détecté : def add_aspect_if_present
            add_aspect_if_present(aspects, planet1, pos1, planet2, pos2, diff, aspect_definitions, aspect_orbs)

    return aspects
    

def format_single_aspect(aspect_name, planet1, pos1, planet2, pos2, ecart):
    """Formate un aspect individuel en texte lisible."""
    return f"« {aspect_name} »  {planet1} ({pos1:.2f}°) et {planet2} ({pos2:.2f}°), avec un écart de « {ecart:.2f}° »."


# Fonction pour formater les aspects en texte lisible avec les positions et l'écart en degrés
def format_aspects_text(aspects, planet_positions):
    # Dictionnaire pour retrouver le nom de la planète à partir de la position
    planet_dict = {position: name for name, position in planet_positions}
    
    formatted_aspects = []
    for aspect_name, pos1, pos2 in aspects:
        planet1 = planet_dict.get(pos1, "Inconnu")
        planet2 = planet_dict.get(pos2, "Inconnu")
        # Appel la focntion : def calculate_angular_difference
        ecart = calculate_angular_difference(pos1, pos2)

        # Appel de la fonction pour formater un aspect individuel ! def format_single_aspect
        formatted_aspects.append(format_single_aspect(aspect_name, planet1, pos1, planet2, pos2, ecart))
   
    return formatted_aspects




# DONNEES DE NAISSANCE
def extract_coordinates(location):
    """Extrait les coordonnées latitude et longitude d'un objet de localisation."""
    latitude = location.latitude
    longitude = location.longitude
    print("Débogage : Coordonnées extraites - latitude:", latitude, ", longitude:", longitude)
    return latitude, longitude

def retrieve_timezone(latitude, longitude):
    """Récupère le fuseau horaire pour des coordonnées données et gère les erreurs éventuelles."""
    timezone_str, error = get_timezone(latitude, longitude)
    if error:
        print("Erreur de fuseau horaire :", error)
    return timezone_str, error


def get_birth_location_data(city_of_birth, country_of_birth):
    # Géolocalisation du lieu de naissance
    location, error = get_location(city_of_birth, country_of_birth)
    if error:
        print("Erreur de géolocalisation :", error)
        return None, None, None, None, error
    
    print("Débogage : Localisation obtenue ->", location)

    # Appel de la fonction pour extraire les coordonnées latitude et longitude : def extract_coordinates
    latitude, longitude = extract_coordinates(location)

    # Appel de la fonction pour récupérer le fuseau horaire : def retrieve_timezone
    timezone_str, error = retrieve_timezone(latitude, longitude)

    
    print("Débogage : Fuseau horaire détecté ->", timezone_str)
    
    return location, latitude, longitude, timezone_str, None


def convert_latlon_to_dms(latitude, longitude):
    # Conversion des coordonnées en DMS (Degrés, Minutes, Secondes)
    latitude_dms = decimal_to_dms(latitude, is_latitude=True)
    longitude_dms = decimal_to_dms(longitude, is_latitude=False)
    print("Débogage : Coordonnées en DMS - latitude_dms:", latitude_dms, ", longitude_dms:", longitude_dms)
    return latitude_dms, longitude_dms


def convert_to_local_and_utc(birth_datetime, timezone_str):
    """Convertit une date de naissance en heures locales et UTC."""
    birth_datetime_local, birth_datetime_utc, error = convert_birth_datetime(birth_datetime, timezone_str)
    if error:
        print("Erreur de conversion datetime :", error)
        return None, None, error

    print("Débogage : Conversion datetime réussie - Heure locale :", birth_datetime_local, ", Heure UTC :", birth_datetime_utc)
    return birth_datetime_local, birth_datetime_utc, None


def calculate_julian_and_positions(birth_datetime_utc):
    # Appel à la fonciotn qui Calcule le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(birth_datetime_utc)
    print("Débogage : Jour julien calculé ->", jd)

    # Appel à la fonciotn qui Calcule les positions des planètes : def calculate_planet_positions(jd):
    results, planet_positions = calculate_planet_positions(jd)
    print("Débogage : Calcul des positions des planètes terminé. Résultats ->", results)

    return jd, results, planet_positions


def generate_aspects_and_text(planet_positions):
    # Calcul des aspects planétaires
    aspects = calculate_astrological_aspects(planet_positions)
    print("Débogage : Calcul des aspects planétaires terminé. Aspects ->", aspects)

    # Formatage du texte des aspects
    aspects_text = format_aspects_text(aspects, planet_positions)
    print("Débogage - aspects_text :", aspects_text)
    
    return aspects, aspects_text


def prepare_theme_data_json(house_results, aspects, planet_positions):
    theme_data_json = json.dumps({
        'houses': house_results,
        'aspects': aspects,
        'planet_positions': planet_positions
    })
    print("Débogage : Contenu de theme_data_json ->", theme_data_json)
    return theme_data_json    


def extract_birth_data_form(request):
    name = request.POST['name']
    birthdate = request.POST['birthdate']
    birthtime = request.POST['birthtime']
    country_of_birth = request.POST['country_of_birth']
    city_of_birth = request.POST['city_of_birth']
    print("Débogage : Variables extraites - name:", name, ", birthdate:", birthdate, ", birthtime:", birthtime)
    print("Débogage : Localisation - ville:", city_of_birth, ", pays:", country_of_birth)
    return name, birthdate, birthtime, country_of_birth, city_of_birth
    

def create_birth_datetime_and_timestamp(birthdate, birthtime):
    birth_datetime_str = f"{birthdate} {birthtime}"
    birth_datetime = datetime.strptime(birth_datetime_str, "%Y-%m-%d %H:%M")
    print("Débogage : birth_datetime construit ->", birth_datetime)

    # Création du timestamp pour rechargement de l'image
    timestamp = int(now().timestamp())
    print("Débogage : Timestamp ajouté ->", timestamp)
    
    return birth_datetime, timestamp


def convert_coordinates_to_dms(latitude, longitude):
    latitude_dms, longitude_dms = convert_latlon_to_dms(latitude, longitude)
    return latitude_dms, longitude_dms


def prepare_template_context(name, results, house_results, aspects, aspects_text, birth_datetime_local, birth_datetime_utc, location, latitude_dms, longitude_dms, theme_data_json):
    return {
        'name': name,
        'results': results,
        'houses': house_results,
        'aspects': aspects,
        'aspects_text': aspects_text,
        'local_year_str': birth_datetime_local.strftime("%Y"),
        'local_time_str': birth_datetime_local.strftime("%H:%M:%S %Z%z"),
        'utc_time_str': birth_datetime_utc.strftime("%H:%M:%S %Z%z"),
        'location': location,
        'latitude_dms': latitude_dms,
        'longitude_dms': longitude_dms,
        'theme_data_json': theme_data_json
    }


def birth_data(request):
    if request.method == 'POST':
        print("Débogage : Vue 'birth_data' appelée.")

        # Appel pour extraire les données du formulaire
        name, birthdate, birthtime, country_of_birth, city_of_birth = extract_birth_data_form(request)
        print("Débogage : Données POST reçues ->", request.POST)

        # Appel pour créer l'objet datetime de naissance et le timestamp
        birth_datetime, timestamp = create_birth_datetime_and_timestamp(birthdate, birthtime)

        # Appel pour obtenir la géolocalisation et le fuseau horaire
        location, latitude, longitude, timezone_str, error = get_birth_location_data(city_of_birth, country_of_birth)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Appel pour convertir les coordonnées en DMS (degrés, minutes, secondes)
        latitude_dms, longitude_dms = convert_coordinates_to_dms(latitude, longitude)

        # Appel pour convertir en heures locales et UTC
        birth_datetime_local, birth_datetime_utc, error = convert_to_local_and_utc(birth_datetime, timezone_str)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Appel pour calculer le jour julien (JD) et les positions des planètes
        jd, results, planet_positions = calculate_julian_and_positions(birth_datetime_utc)

        # Appel pour calculer les maisons astrologiques
        house_results = calculate_astrological_houses(jd, latitude, longitude)
        print("Débogage : Calcul des maisons astrologiques terminé.")

        # Appel pour calculer les aspects planétaires et formater le texte des aspects
        aspects, aspects_text = generate_aspects_and_text(planet_positions)
        
        print("Avant enregistrement - Type et valeur de planet_positions :", type(planet_positions), planet_positions)
        print("Avant enregistrement - Type et valeur de aspects :", type(aspects), aspects)
        print("Avant enregistrement - Type et valeur de house_results :", type(house_results), house_results)


        # Appel pour préparer les données du thème en JSON pour le template
        theme_data_json = prepare_theme_data_json(house_results, aspects, planet_positions)
        
        print("Après enregistrement - Type et valeur de planet_positions :", type(planet_positions), planet_positions)
        print("Après enregistrement - Type et valeur de aspects :", type(aspects), aspects)
        print("Après enregistrement - Type et valeur de house_results :", type(house_results), house_results)


        # Appel pour générer la roue astrologique visuelle
        print("Débogage : Génération de la roue astrologique.")
        generate_astrological_wheel(planet_positions, house_results, aspects)

        # Appel pour préparer le contexte à transmettre au template
        context = prepare_template_context(
            name, results, house_results, aspects, aspects_text,
            birth_datetime_local, birth_datetime_utc, location,
            latitude_dms, longitude_dms, theme_data_json
        )

        print("Débogage : Contenu de context avant rendu :", context)

        return render(request, 'birth_results.html', context)

    # Affichage du formulaire pour une requête GET
    print("Débogage : Affichage du formulaire 'birth_data_form.html'.")
    return render(request, 'birth_data_form.html')






# PLANETES & MAISONS
def extract_request_parameters(request):
    """Extrait les paramètres de date, ville et pays depuis la requête GET."""
    selected_date = request.GET.get('date')
    city_of_birth = request.GET.get('city_of_birth')
    country_of_birth = request.GET.get('country_of_birth')
    return selected_date, city_of_birth, country_of_birth


def geolocate_city(city, country):
    """Géolocalise une ville et un pays et retourne la latitude, longitude et une erreur éventuelle."""
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city}, {country}", timeout=10)
    if not location:
        error_message = "Lieu de naissance introuvable. Veuillez vérifier l'orthographe ou entrer un autre lieu."
        print("Erreur :", error_message)
        return None, None, error_message

    print(f"Débogage : Résultat de la géolocalisation - Latitude: {location.latitude}, Longitude: {location.longitude}")
    return location.latitude, location.longitude, None


def determine_timezone(city, country, latitude, longitude):
    """Détermine le fuseau horaire pour une ville et un pays donnés, avec un cas particulier pour Cayenne."""
    if city.lower() == "cayenne" and country.lower() in ["guyane française", "french guiana"]:
        timezone_at = "Etc/GMT+3"  # UTC-3 pour Cayenne
        print("Débogage : Fuseau horaire pour Cayenne forcé à UTC-3")
    else:
        tf = TimezoneFinder()
        timezone_at = tf.timezone_at(lng=longitude, lat=latitude)
        print(f"Debug - Fuseau horaire détecté par TimezoneFinder : {timezone_at}")

    if not timezone_at:
        error_message = "Impossible de déterminer le fuseau horaire pour ce lieu."
        print("Erreur :", error_message)
        return None, error_message

    return timezone_at, None


def convert_to_utc(date_obj, timezone_str):
    """Convertit un objet datetime en UTC selon le fuseau horaire fourni."""
    try:
        # Applique le fuseau horaire local fourni pour convertir la date en UTC
        local_tz = pytz.timezone(timezone_str)
        print(f"Debug - Application du fuseau horaire : {timezone_str}")
        
        # Si l'objet date n'a pas encore de fuseau horaire, applique local_tz
        if date_obj.tzinfo is None:
            date_obj = local_tz.localize(date_obj)
        
        # Conversion en UTC
        date_utc = date_obj.astimezone(pytz.utc)
        print(f"Debug - Date locale après application du fuseau : {date_obj}, Date UTC : {date_utc}")
        
        return date_utc, None

    except Exception as e:
        error_message = f"Erreur de conversion du fuseau horaire : {e}"
        print(error_message)
        return None, error_message


# Fonction pour extraire les informations de date
def extract_date_info(selected_date):
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    local_day_str = date_obj.day
    local_month_str = date_obj.strftime("%B")  # Mois sous forme de texte (ex: Janvier)
    local_year_str = date_obj.year
    print(f"Débogage : Jour -> {local_day_str}, Mois -> {local_month_str}, Année -> {local_year_str}")
    return date_obj, local_day_str, local_month_str, local_year_str


# Fonction pour préparer le contexte de rendu HTML
def prepare_planetary_context(selected_date, city_of_birth, country_of_birth, local_day_str, local_month_str, local_year_str, results, house_results):
    return {
        'selected_date': selected_date,
        'city_of_birth': city_of_birth,
        'country_of_birth': country_of_birth,
        'local_day_str': local_day_str,
        'local_month_str': local_month_str,
        'local_year_str': local_year_str,
        'results': results,
        'houses': house_results,
    }

# Fonction pour calculer les positions planétaires et les maisons
def calculate_positions_and_houses(jd, latitude, longitude):
    results, planet_positions = calculate_planet_positions(jd)
    house_results = calculate_houses(jd, latitude, longitude)
    
    # Debugging: Afficher les résultats calculés
    print(f"Debug - Résultats des positions planétaires: {results}")
    print(f"Debug - Résultats des maisons astrologiques: {house_results}")
    
    return results, planet_positions, house_results


# Position des Planètes
def planetary_position(request):# Calculer le jour julien (JD)
    # Appel de la foction : def extract_request_parameters
    selected_date, city_of_birth, country_of_birth = extract_request_parameters(request)

    # Vérifier si les champs requis sont fournis
    if not selected_date or not city_of_birth or not country_of_birth:
        print("Erreur : Champs manquants - date:", selected_date, ", ville:", city_of_birth, ", pays:", country_of_birth)
        return HttpResponse("Tous les champs (date, ville de naissance, pays de naissance) doivent être renseignés.")
    
    print("Débogage : Variables reçues - date:", selected_date, ", ville:", city_of_birth, ", pays:", country_of_birth)

    # Appel de la fonction pour extraire les informations de date : def extract_date_info
    date_obj, local_day_str, local_month_str, local_year_str = extract_date_info(selected_date)

    # Utiliser le geolocator pour obtenir la latitude et la longitude
    print("Debug - Tentative de géolocalisation avec geolocator")
    latitude, longitude, error = geolocate_city(city_of_birth, country_of_birth)
    if error:
        return HttpResponse(error)

    # Debugging: Afficher les valeurs de latitude et longitude
    print(f"Debug - Latitude: {latitude}, Longitude: {longitude}")
    print(f"Debug - Ville de naissance: {city_of_birth}, Pays de naissance: {country_of_birth}")


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


# 8-Fonction pour convertir les coordonnées en DMS
def decimal_to_dms(coordinate, is_latitude=True):
    if is_latitude:
        direction = 'N' if coordinate >= 0 else 'S'
    else:
        direction = 'E' if coordinate >= 0 else 'O'
    abs_coord = abs(coordinate)
    degrees = int(abs_coord)
    minutes = int((abs_coord - degrees) * 60)
    seconds = (abs_coord - degrees - minutes / 60) * 3600
    return f"{degrees}° {minutes}' {seconds:.2f}\" {direction}"
    
    

    
# ROUE
def extract_wheel_data(request):
    """Extrait les données de la roue astrologique des paramètres GET."""
    house_results = json.loads(request.GET.get('house_results', '{}'))
    aspects = json.loads(request.GET.get('aspects', '[]'))
    planet_positions = json.loads(request.GET.get('planet_positions', '[]'))
    return house_results, aspects, planet_positions

def prepare_aspects_text(aspects, planet_positions):
    """Prépare le texte formaté des aspects pour l'affichage."""
    return format_aspects_text(aspects, planet_positions)

def prepare_wheel_context(planet_positions, house_results, aspects_text):
    """Prépare le contexte pour le rendu de la roue astrologique."""
    return {
        'results': planet_positions,
        'houses': house_results,
        'aspects_text': aspects_text
    }

def display_astrological_wheel(request):
    # Appel de la fonciton pour Charger les données depuis les paramètres GET : def extract_wheel_data
    house_results, aspects, planet_positions = extract_wheel_data(request)


    # Ajout de débogages pour vérifier les données reçues
    print("House Results:", house_results)
    print("Aspects:", aspects)
    print("Planet Positions:", planet_positions)

    # Appel de la fonciotn pour Formater les aspects en texte lisible : def prepare_aspects_text
    aspects_text = prepare_aspects_text(aspects, planet_positions)
    print("Débogage - aspects_text après formatage :", aspects_text)  # Vérifier le contenu formaté

    # Appel de la fonction pour préparer le contexte pour le rendu et passer les données formatées au template : def prepare_wheel_contex
    context = prepare_wheel_context(planet_positions, house_results, aspects_text)
    return render(request, 'birth_results.html', context)



# Fonction générale pour appeler les sous foncitons.
def generate_astrological_wheel(planet_positions, house_results, aspects):
    # Définir le chemin d'image
    image_path = os.path.join(settings.BASE_DIR, 'astroapp/static/images/zodiac_wheel.png')

    # Initialiser la figure et les axes
    fig, ax = create_astrological_figure()

    # Calculer l’offset de rotation pour aligner l'ascendant à gauche
    asc_angle = house_results['Maison 1']['degree']
    rotation_offset = np.radians(-asc_angle + 180)

    # Dessiner le cercle principal
    draw_circle(ax)

    # Dessiner les segments colorés des signes
    draw_segments(ax, rotation_offset)

    # Ajouter les divisions principales et les subdivisions
    draw_divisions(ax, rotation_offset)

    # Placer les symboles des signes du zodiaque
    draw_zodiac_symbols(ax, rotation_offset)

    # Positionner les symboles des planètes selon leurs positions calculées et ajouter les lignes de liaison
    draw_planet_positions(ax, planet_positions, rotation_offset)

    # Ajouter les cuspides des maisons et les triangles pour les maisons principales
    draw_houses_and_cusps(ax, house_results, rotation_offset)

    # Afficher les degrés et minutes pour chaque planète et chaque maison
    display_degrees(ax, planet_positions, house_results, rotation_offset)

    # Ajouter les lignes pour l'ASC et le MC avec leurs marqueurs
    draw_asc_mc_lines(ax, house_results, rotation_offset)

    # Ajouter les numéros des maisons
    draw_house_numbers(ax, house_results, rotation_offset)
    
    # Appeler draw_aspects pour dessiner les aspects
    draw_aspects(ax, aspects, rotation_offset)


    # Ajuster les limites de l'axe pour ne pas couper les angles
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-2.9, 2.9)

    # Supprimer les marges automatiques et régler la figure pour occuper tout l'espace
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.set_size_inches(12, 12)
    ax.set_aspect('equal')
    
    # Sauvegarder l'image finale
    save_astrological_image(fig, image_path)


def create_astrological_figure():
    # Créer la figure et les axes avec la taille et les limites appropriées
    fig, ax = plt.subplots(figsize=(14, 14))  # Dimensions de la figure (modifiables si nécessaire)
    ax.set_xlim(-1.5, 1.5)  # Limites de l'axe x
    ax.set_ylim(-1.5, 1.5)  # Limites de l'axe y
    ax.set_aspect('equal')  # Proportions égales pour un cercle parfait
    ax.axis('off')  # Masquer les axes pour un rendu propre de la roue astrologique
    
    return fig, ax


def draw_circle(ax):
    # Dessiner le cercle principal qui forme la base de la roue astrologique
    main_circle = plt.Circle((0, 0), 1.2, edgecolor='black', facecolor='none', linewidth=1)
    ax.add_patch(main_circle)
    
    # Ajouter un cercle blanc au centre pour dégager la zone centrale
    center_circle = plt.Circle((0, 0), 0.80, color='white', ec='black', linewidth=0.5, zorder=10)
    ax.add_patch(center_circle)
    
    # Ajouter un cercle extérieur pour la bordure de la roue
    outer_border_circle = plt.Circle((0, 0), 1.2, color='none', ec='black', linewidth=0.5, zorder=5)
    ax.add_patch(outer_border_circle)

def get_segment_colors():
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]
    return colors_outer, colors_inner

def draw_single_segment(ax, color_outer, color_inner, theta1, theta2):
    """Dessine un segment astrologique en deux arcs (extérieur et intérieur) avec des couleurs spécifiques."""
    # Dessiner l'arc extérieur
    arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
    ax.add_patch(arc_outer)

    # Dessiner l'arc intérieur
    arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
    ax.add_patch(arc_inner)

def draw_segments(ax, rotation_offset):
    # Appel de la fonciton pour les Couleurs des segments par élément (feu, terre, air, eau) : def get_segment_colors
    colors_outer, colors_inner = get_segment_colors()

    # Dessiner chaque segment pour les 12 signes
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        # Calculer l'angle de début pour chaque segment
        angle = 2 * np.pi / 12 * i
        angle_corrected = angle + rotation_offset

        # Définir les angles de chaque arc en degrés
        theta1 = np.degrees(angle_corrected)
        theta2 = np.degrees(angle_corrected + 2 * np.pi / 12)

        # Appel de la fonction pour Dessiner les arcs extérieur et intérieur pour chaque segment : def draw_single_segment
        draw_single_segment(ax, color_outer, color_inner, theta1, theta2)

def draw_main_divisions(ax, rotation_offset):
    """Dessine les divisions principales de 30° pour chaque signe."""
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        angle_corrected = angle + rotation_offset
        x_outer = 1.2 * np.cos(angle_corrected)
        y_outer = 1.2 * np.sin(angle_corrected)
        x_inner = 0.8 * np.cos(angle_corrected)
        y_inner = 0.8 * np.sin(angle_corrected)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)

def draw_subdivisions(ax, rotation_offset):
    """Dessine les subdivisions de 5° entre chaque division principale."""
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            sub_angle_corrected = sub_angle + rotation_offset
            x_sub = 1.2 * np.cos(sub_angle_corrected)
            y_sub = 1.2 * np.sin(sub_angle_corrected)
            x_sub_inner = 1.1 * np.cos(sub_angle_corrected)
            y_sub_inner = 1.1 * np.sin(sub_angle_corrected)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)


def draw_divisions(ax, rotation_offset):
    # Appel de la fonction pour ajouter les divisions principales de 30° pour chaque signe : def draw_main_divisions
    draw_main_divisions(ax, rotation_offset)

    # Appel de la fonction pour ajouter les subdivisions de 5° entre chaque division principale : def draw_subdivisions
    draw_subdivisions(ax, rotation_offset)


def get_zodiac_data():
    """Retourne les éléments, les couleurs et les symboles des signes du zodiaque."""
    elements = ['fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water']

    sign_colors = {
        'fire': "#f9074c",   # Bélier, Lion, Sagittaire
        'earth': "#c59626",  # Taureau, Vierge, Capricorne
        'air': "#1a8fe9",    # Gémeaux, Balance, Verseau
        'water': "#62ce02"   # Cancer, Scorpion, Poissons
    }

    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    return elements, sign_colors, zodiac_symbols

def load_zodiac_font():
    """Charge et retourne la police HamburgSymbols pour les symboles du zodiaque."""
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    return font_manager.FontProperties(fname=font_path)


def draw_zodiac_symbols(ax, rotation_offset):
    # Appel de la fonciton pour associer les éléments aux signes du zodiaque : def get_zodiac_data
    elements, sign_colors, zodiac_symbols = get_zodiac_data()


    # Liste des symboles zodiacaux (en utilisant des symboles unicode ou police spécifique)
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    
    # Appel de la fonciton pour Charger la police HamburgSymbols si nécessaire : def load_zodiac_font
    prop = load_zodiac_font()


    # Placer chaque symbole du zodiaque
    for i, symbol in enumerate(zodiac_symbols):
        # Calculer l'angle de positionnement pour chaque signe
        angle = np.radians(30 * i + 15)
        angle_corrected = angle + rotation_offset
        x_text = 0.96 * np.cos(angle_corrected)
        y_text = 0.96 * np.sin(angle_corrected)

        # Déterminer la couleur du signe en fonction de son élément
        element = elements[i]
        symbol_color = sign_colors[element]

        # Définir la taille du symbole zodiacal en fonction de la figure
        symbol_size = 40  # Ajustable si nécessaire

        # Ajouter le symbole à la figure
        ax.text(x_text, y_text, symbol, fontsize=symbol_size, 
                ha='center', va='center', fontproperties=prop, color=symbol_color)


def get_planet_data():
    """Retourne les symboles et couleurs des planètes."""
    planet_symbols = {
        'Soleil': 'Q', 'Lune': 'W', 'Mercure': 'E', 'Vénus': 'R', 
        'Mars': 'T', 'Jupiter': 'Y', 'Saturne': 'U', 'Uranus': 'I', 
        'Neptune': 'O', 'Pluton': 'P'
    }
    
    planet_colors = {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }
    
    return planet_symbols, planet_colors


def place_planet(ax, planet, degree, rotation_offset, prop, planet_symbols, planet_colors):
    """Place une planète à sa position correcte et trace la ligne de liaison."""
    # Calcul de l'angle de la planète en radians
    angle = np.radians(degree)
    angle_corrected = angle + rotation_offset
    x = 1.7 * np.cos(angle_corrected)
    y = 1.7 * np.sin(angle_corrected)
    
    # Récupérer le symbole et la couleur de la planète
    symbol = planet_symbols.get(planet, "?")
    color = planet_colors.get(planet, '#000000')  # Couleur noire par défaut si aucune correspondance

    # Ajouter le symbole de la planète avec sa couleur et sa position
    ax.text(x, y, symbol, fontproperties=prop, fontsize=40, color=color, 
            ha='center', va='center')
    
    # Tracer une ligne de liaison entre le centre et la position de la planète
    ax.plot([0, 0.9 * x], [0, 0.9 * y], color='black', lw=0.5, zorder=1)


def draw_planet_positions(ax, planet_positions, rotation_offset):
    # Appel de la fonction pour récupérer les symboles et couleurs des planètes : def get_planet_data
    planet_symbols, planet_colors = get_planet_data()

    # Police HamburgSymbols pour les symboles planétaires
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

    # Placer chaque planète à sa position respective et ajouter les lignes de liaison
    for planet, degree in planet_positions:
        
        # Appel de la fonction pour placer chaque planète : def place_planet
        place_planet(ax, planet, degree, rotation_offset, prop, planet_symbols, planet_colors)

# Les lignes
def add_house_cusps(ax, house_results, rotation_offset):
    """Ajoute les lignes de cuspides pour chaque maison sur la roue astrologique."""
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle en degrés pour chaque cuspide de maison
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Calculer la position pour la ligne de la cuspide de la maison
        x_pos = 1.27 * np.cos(angle_corrected)
        y_pos = 1.27 * np.sin(angle_corrected)
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)  # Ligne de cuspide de maison
        
# Les Triangles
def add_house_triangles(ax, house_results, rotation_offset):
    """Ajoute les triangles pour marquer les cuspides des maisons principales et secondaires."""
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle_corrected = np.radians(degree) + rotation_offset
        x_triangle = 1.26 * np.cos(angle_corrected)
        y_triangle = 1.26 * np.sin(angle_corrected)
        facecolor = 'black' if i + 1 in [1, 4, 7, 10] else 'white'
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05,
                                          orientation=angle_corrected + np.pi / 2,
                                          edgecolor='black', facecolor=facecolor,
                                          linewidth=1.0, zorder=3)
        ax.add_patch(triangle)
               
# Les lignes et les triangles
def draw_houses_and_cusps(ax, house_results, rotation_offset):
    # Appel de la fonction pour ajouter les LIGNES de cuspides pour chaque maison : def add_house_cusps
    add_house_cusps(ax, house_results, rotation_offset)

    # Appel de la fonction pour ajouter les TRIANGLES pour chaque maison : def add_house_triangles
    add_house_triangles(ax, house_results, rotation_offset)


def get_planet_colors():
    """Retourne le dictionnaire des couleurs pour chaque planète."""
    return {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }


def display_planet_degrees(ax, planet_positions, rotation_offset, planet_colors):
    """Affiche les degrés et minutes pour chaque planète sur la roue astrologique."""
    for planet, degree in planet_positions:
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        degree_in_sign = degree % 30
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        x_degree = 1.94 * np.cos(angle_corrected)
        y_degree = 1.94 * np.sin(angle_corrected)
        
        x_minutes = 2.10 * np.cos(angle_corrected)
        y_minutes = 2.10 * np.sin(angle_corrected)
        
        degree_color = planet_colors.get(planet, 'black')

        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=13, 
                ha='center', va='center', color=degree_color, weight='bold')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=11, 
                ha='center', va='center', color=degree_color, weight='bold')


def display_house_degrees(ax, house_results, rotation_offset):
    """Affiche les degrés et minutes pour chaque cuspide de maison sur la roue astrologique."""
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        degree_in_sign = degree % 30
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        x_degree = 1.38 * np.cos(angle_corrected)
        y_degree = 1.38 * np.sin(angle_corrected)
        
        x_minutes = 1.5 * np.cos(angle_corrected)
        y_minutes = 1.5 * np.sin(angle_corrected)
        
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=11, 
                ha='center', va='center', color='black')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, 
                ha='center', va='center', color='black')


def display_degrees(ax, planet_positions, house_results, rotation_offset):
    # Appelle de la fonction du Dictionnaire des couleurs des planètes : def get_planet_colors
    planet_colors = get_planet_colors()

    # Appelle de la fonction pour l'Affichage des degrés pour chaque planète : def display_planet_degrees
    display_planet_degrees(ax, planet_positions, rotation_offset, planet_colors)

    # Appelle de la fonction pour l'Affichage des degrés pour chaque cuspide de maison (en noir) : def display_house_degrees
    display_house_degrees(ax, house_results, rotation_offset)



def draw_asc_mc_marker(ax, label, degree, rotation_offset):
    """Dessine la ligne, le marqueur et le label pour l'ASC ou le MC."""
    angle = np.radians(degree)
    angle_corrected = angle + rotation_offset
    x_pos = 2.3 * np.cos(angle_corrected)
    y_pos = 2.3 * np.sin(angle_corrected)

    ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.5, zorder=1)

    if label == 'ASC':
        triangle = patches.RegularPolygon((x_pos, y_pos), numVertices=3, radius=0.20,
                                          orientation=angle_corrected + np.radians(270),
                                          edgecolor='black', facecolor='white', lw=0.5, zorder=3)
        ax.add_patch(triangle)
        ax.text(x_pos + 0.4 * np.cos(angle_corrected), y_pos + 0.4 * np.sin(angle_corrected), 
                'ASC', fontsize=12, ha='center', va='center', color='black', weight='bold')

    elif label == 'MC':
        circle = plt.Circle((x_pos, y_pos), 0.20, facecolor='white', edgecolor='black', lw=0.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x_pos + 0.35 * np.cos(angle_corrected), y_pos + 0.35 * np.sin(angle_corrected), 
                'MC', fontsize=12, ha='center', va='center', color='black', weight='bold')


def draw_asc_mc_lines(ax, house_results, rotation_offset):
    # Dictionnaire pour associer ASC et MC aux maisons
    asc_mc_houses = {'ASC': 'Maison 1', 'MC': 'Maison 10'}

    # Ajouter une ligne et un marqueur pour chaque élément (ASC et MC)
    for label, house_key in asc_mc_houses.items():
        # Récupérer le degré de la maison associée (Maison 1 pour ASC, Maison 10 pour MC)
        degree = house_results[house_key]['degree']

        # Appel de la fonction pour dessiner la ligne, le marqueur et le label
        draw_asc_mc_marker(ax, label, degree, rotation_offset)




def get_roman_numerals():
    """Renvoie un dictionnaire associant les numéros de maisons aux chiffres romains."""
    return {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }


def calculate_house_position(degree_start, degree_end, rotation_offset):
    """Calcule la position x, y pour un numéro de maison au centre de son segment."""
    if degree_end < degree_start:
        degree_end += 360
    degree_mid = (degree_start + degree_end) / 2
    angle_mid = np.radians(degree_mid) + rotation_offset
    x_text = 1.28 * np.cos(angle_mid)
    y_text = 1.28 * np.sin(angle_mid)
    return x_text, y_text

def draw_house_numbers(ax, house_results, rotation_offset):
    # Dictionnaire pour convertir les numéros de maisons en chiffres romains


    # Positionner chaque numéro de maison au centre de son segment
    for i in range(len(house_results)):
        # Obtenir les angles des cuspides de chaque maison
        degree_start = house_results[f'Maison {i + 1}']['degree']
        degree_end = house_results[f'Maison {(i + 2) if (i + 2) <= 12 else 1}']['degree']
        
        # Appel de la fonciton pour Ajuster si le segment traverse 0° : def calculate_house_position
        x_text, y_text = calculate_house_position(degree_start, degree_end, rotation_offset)
        
        # Appel de la fonciton pour Afficher le numéro de maison au centre de chaque segment : def get_roman_numerals
        roman_house_num = get_roman_numerals()[i + 1]
        
        ax.text(x_text, y_text, roman_house_num, fontsize=12, ha='center', va='center', color='black', weight='bold')


def get_aspect_style(type_aspect):
    """Retourne le style pour le type d'aspect donné, ou None si non défini."""
    aspect_styles = {
        'Opposition': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},
        'Trigone': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
        'Carré': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},
        'Sextile': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
    }
    return aspect_styles.get(type_aspect)


def calculate_aspect_positions(pos1, pos2, rotation_offset):
    """Calcule les positions corrigées pour les lignes d'aspect en fonction de l'angle et du décalage."""
    angle1 = np.radians(pos1) + rotation_offset
    angle2 = np.radians(pos2) + rotation_offset
    x1, y1 = 0.8 * np.cos(angle1), 0.8 * np.sin(angle1)
    x2, y2 = 0.8 * np.cos(angle2), 0.8 * np.sin(angle2)
    return x1, y1, x2, y2


def draw_aspects(ax, aspects, rotation_offset):
    """
    Dessine les aspects astrologiques entre les planètes sur la roue astrologique.

    Paramètres :
    - ax : objet Axe de Matplotlib sur lequel la roue astrologique est dessinée.
    - aspects : liste de tuples contenant les informations sur chaque aspect. 
                Chaque tuple est de la forme (type_aspect, pos1, pos2),
                où type_aspect est le type d'aspect ('opposition', 'trigone', etc.)
                et pos1, pos2 sont les positions angulaires des deux planètes en degrés.
    - rotation_offset : décalage angulaire pour aligner les aspects sur la roue.
    """
    # Paramètres de style pour chaque type d'aspect
    aspect_styles = {
        'Opposition': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},  # Tirets longs
        'Trigone': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
        'Carré': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},  # Tirets longs
        'Sextile': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
    }

    for aspect in aspects:
        type_aspect, pos1, pos2 = aspect
        # Appel de la fonciotn pour Obtenir le style pour le type d'aspect : def get_aspect_style
        style = get_aspect_style(type_aspect)
        if not style:
            continue


        # Appel de la fonciotn pour Appliquer le décalage de rotation et... :  def calculate_aspect_positions
        # Calculer les positions des extrémités des lignes d'aspect
        x1, y1, x2, y2 = calculate_aspect_positions(pos1, pos2, rotation_offset)


        # Dessiner la ligne d'aspect
        ax.plot([x1, x2], [y1, y2], color=style['color'], linestyle=style['linestyle'], linewidth=style['linewidth'], zorder=10)



def deserialize_wheel_data(house_results_str, aspects_str, planet_positions_str):
    """Désérialise les données JSON pour les maisons, les aspects et les positions planétaires."""
    try:
        house_results = json.loads(house_results_str)
        aspects = json.loads(aspects_str)
        planet_positions = json.loads(planet_positions_str)
    except json.JSONDecodeError as e:
        # Si erreur de désérialisation, initialiser avec des valeurs vides
        house_results, aspects, planet_positions = {}, [], []
        print("Erreur de désérialisation :", e)

    # Afficher les données après désérialisation pour vérification
    print("Débogage - house_results:", house_results)
    print("Débogage - aspects:", aspects)
    print("Débogage - planet_positions:", planet_positions)

    return house_results, aspects, planet_positions


def birth_results(request):
    # Récupération simplifiée des données de thème
    house_results = {}
    aspects = []
    planet_positions = {}

    # Affichage pour vérification (optionnel)
    print("Données pour Affichage :", {
        'house_results': house_results,
        'aspects': aspects,
        'planet_positions': planet_positions,
    })

    # Rendre les données au template
    return render(request, 'birth_results.html', {
        'house_results': house_results,
        'aspects': aspects,
        'planet_positions': planet_positions,
    })






# FIN 
def remove_existing_image(image_path):
    """Supprime l'image existante à un chemin donné si elle est présente."""
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Ancienne image supprimée : {image_path}")
    else:
        print(f"Aucune ancienne image à supprimer : {image_path}")


def save_astrological_image(fig, image_path):

    # Appel de la fonction pour supprimer l'image existante si elle existe : def remove_existing_image
    remove_existing_image(image_path)


    # Sauvegarder la nouvelle image générée
    try:
        fig.savefig(image_path, dpi=300)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")
    finally:
        plt.close(fig)  # Fermer la figure pour libérer la mémoire

