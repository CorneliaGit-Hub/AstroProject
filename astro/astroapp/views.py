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
from django.http import JsonResponse
from django.contrib import messages  # Import pour les messages flash

from astroapp.utils.geolocation_utils import (
    get_location,
    get_timezone,
    localize_datetime,
    extract_coordinates,
    retrieve_timezone,
    get_birth_location_data,
    geolocate_city,
    determine_timezone,
    extract_date_info
)
from astroapp.utils.conversions_utils import (
    convert_to_dms,
    convert_to_utc,
    convert_birth_datetime,
    convert_latlon_to_dms,
    decimal_to_dms,
    convert_to_local_and_utc,
    create_birth_datetime_and_timestamp,
    convert_coordinates_to_dms,
)
from astroapp.utils.zodiac_utils import (
    get_zodiac_sign,
    get_zodiac_data,
    load_zodiac_font
)

from astroapp.utils.planet_utils import (
    get_planet_data,
    place_planet,
    draw_planet_positions
)
from astroapp.utils.data_utils import (
    format_single_aspect,
    prepare_theme_data_json,
    prepare_wheel_context,
    prepare_planetary_context,
    extract_request_parameters,
    extract_wheel_data,
    deserialize_wheel_data,
)
from astroapp.calculs.aspects_calculations import (
    calculate_angular_difference,
    add_aspect_if_present,
    calculate_aspects,
    calculate_astrological_aspects,
)
from astroapp.calculs.planet_calculations import (
    calculate_single_planet_position,
    calculate_planet_positions,
    format_planet_positions,
)
from astroapp.calculs.ephemeris_calculations import (
    calculate_julian_day,
    calculate_julian_day_and_planet_positions,
    calculate_julian_and_positions,
)
from astroapp.calculs.houses_calculations import (
    format_house_cusp,
    get_asc_mc,
    calculate_houses,
    calculate_astrological_houses,
    calculate_positions_and_houses,
)
from astroapp.wheel.wheel_symbols import (
    draw_zodiac_symbols,
    get_planet_colors,
    display_planet_degrees,
)
from astroapp.wheel.wheel_aspects import (
    get_aspect_style,
    calculate_aspect_positions,
    draw_aspects,
)

from astroapp.wheel.wheel_houses import add_house_cusps
from astroapp.wheel.wheel_houses import add_house_triangles
from astroapp.wheel.wheel_houses import draw_houses_and_cusps
from astroapp.wheel.wheel_houses import display_house_degrees
from astroapp.wheel.wheel_houses import get_roman_numerals
from astroapp.wheel.wheel_houses import calculate_house_position
from astroapp.wheel.wheel_houses import draw_house_numbers


from astroapp.wheel.wheel_segments import get_segment_colors
from astroapp.wheel.wheel_segments import draw_single_segment
from astroapp.wheel.wheel_segments import draw_segments
from astroapp.wheel.wheel_segments import draw_main_divisions
from astroapp.wheel.wheel_segments import draw_subdivisions
from astroapp.wheel.wheel_segments import draw_divisions


from astroapp.wheel.wheel_core import create_astrological_figure
from astroapp.wheel.wheel_core import draw_circle





































# Test rapide
test_date = datetime(2023, 11, 21, 12, 0, 0)


# ENREGISTRER UN THEME
def enregistrer_naissance(request):
    """
    Récupère les données de la session, les valide et les enregistre en base.
    """
    if request.method == "POST":

        # Récupération des données en session
        name = request.session.get("name")
        birthdate = request.session.get("birthdate")
        birthtime = request.session.get("birthtime")
        country_of_birth = request.session.get("country_of_birth")
        city_of_birth = request.session.get("city_of_birth")

        # Affichage des données dans les logs
        print("Débogage - Données récupérées pour l'enregistrement :")
        print(f"Nom : {name}")
        print(f"Date de naissance : {birthdate}")
        print(f"Heure de naissance : {birthtime}")
        print(f"Pays de naissance : {country_of_birth}")
        print(f"Ville de naissance : {city_of_birth}")

        # Vérification que toutes les données sont présentes
        if not all([name, birthdate, birthtime, country_of_birth, city_of_birth]):
            return JsonResponse({
                "success": False,
                "message": "Certaines données nécessaires sont manquantes."
            }, json_dumps_params={'ensure_ascii': False})

        # Enregistrement en base de données
        try:
            ThemeAstrologique.objects.create(
                utilisateur=request.user,  # Utilisateur connecté
                name=name,
                birthdate=birthdate,
                birthtime=birthtime,
                country_of_birth=country_of_birth,
                city_of_birth=city_of_birth,
            )
            print("Débogage - Enregistrement réussi dans la base de données.")
            return JsonResponse({
                "success": True,
                "message": "Thème enregistré avec succès !"
            }, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            print(f"Erreur lors de l'enregistrement en base : {str(e)}")
            return JsonResponse({
                "success": False,
                "message": f"Erreur lors de l'enregistrement : {str(e)}"
            }, json_dumps_params={'ensure_ascii': False})

    # Si la méthode utilisée n'est pas POST
    print("Débogage - Requête non POST détectée.")
    return JsonResponse({
        "success": False,
        "message": "Méthode non autorisée."
    }, json_dumps_params={'ensure_ascii': False})



def stocker_donnees_session(request, data):
    """
    Stocke les données fournies dans la session Django.
    Args:
        request: La requête HTTP.
        data: Un dictionnaire contenant les données à stocker.
    """
    for key, value in data.items():
        request.session[key] = value
    print("Données stockées en session :", request.session.items())  # Vérification dans la console

def extract_form_data(request):
    """
    Extrait les données du formulaire POST pour les stocker.
    Args:
        request: La requête HTTP contenant les données du formulaire.
    Returns:
        Un dictionnaire avec les données extraites ou une valeur par défaut si elles sont absentes.
    """
    return {
        "name": request.POST.get("name", "Non défini"),
        "birthdate": request.POST.get("birthdate", "Non défini"),
        "birthtime": request.POST.get("birthtime", "Non défini"),
        "country_of_birth": request.POST.get("country_of_birth", "Non défini"),
        "city_of_birth": request.POST.get("city_of_birth", "Non défini"),
    }


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




# JULIAN DAY 



    

    


# PLANETES 







    



# ZODIAQUE
# Fonction pour retourner l'image de la roue zodiacale
def zodiac_wheel(request):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'zodiac_wheel.png')
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/png")









# MAISONS












# GEOLOCALISATION





















# ASPECTS










    

# RESTE DANS VIEWS
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


# RESTE DANS VIEWS
def generate_aspects_and_text(planet_positions):
    # Calcul des aspects planétaires
    aspects = calculate_astrological_aspects(planet_positions)


    # Formatage du texte des aspects
    aspects_text = format_aspects_text(aspects, planet_positions)

    
    return aspects, aspects_text





def extract_birth_data_form(request):
    name = request.POST['name']
    birthdate = request.POST['birthdate']
    birthtime = request.POST['birthtime']
    country_of_birth = request.POST['country_of_birth']
    city_of_birth = request.POST['city_of_birth']
    print("Débogage : Variables extraites - name:", name, ", birthdate:", birthdate, ", birthtime:", birthtime)
    print("Débogage : Localisation - ville:", city_of_birth, ", pays:", country_of_birth)
    return name, birthdate, birthtime, country_of_birth, city_of_birth
    







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

        # Appel pour extraire les données du formulaire
        print("Débogage : Données extraites :", request.POST)
        donnees = extract_form_data(request)

        # Appel pour stocker les données en session
        print("Débogage : Appel à stocker_donnees_session")
        stocker_donnees_session(request, donnees)

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


        # Appel pour calculer les aspects planétaires et formater le texte des aspects
        aspects, aspects_text = generate_aspects_and_text(planet_positions)
       

        # Appel pour préparer les données du thème en JSON pour le template
        theme_data_json = prepare_theme_data_json(house_results, aspects, planet_positions)   


        # Appel pour générer la roue astrologique visuelle

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








# RESTE DANS VIEWS
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



    
    

    
# ROUE

# RESTE DANS VIEWS
def prepare_aspects_text(aspects, planet_positions):
    """Prépare le texte formaté des aspects pour l'affichage."""
    return format_aspects_text(aspects, planet_positions)



def display_astrological_wheel(request):
    # Appel de la fonciton pour Charger les données depuis les paramètres GET : def extract_wheel_data
    house_results, aspects, planet_positions = extract_wheel_data(request)

    # Appel de la fonciotn pour Formater les aspects en texte lisible : def prepare_aspects_text
    aspects_text = prepare_aspects_text(aspects, planet_positions)


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

