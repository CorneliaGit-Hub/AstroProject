import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
from django.shortcuts import render
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

# PLANETES DEF
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

    for planet_name, planet_id in planets.items():
        position, _ = swe.calc_ut(jd, planet_id)
        degree = position[0]
        sign, sign_degree = get_zodiac_sign(degree)
        results[planet_name] = {
            'degree': degree,
            'sign': sign,
            'sign_degree': sign_degree,
        }
        planet_positions.append((planet_name, degree))

    return results, planet_positions

# 2-Fonction pour convertir les degrés en degrés, minutes et secondes
def convert_to_dms(degree):
    degrees = int(degree)
    minutes = int((degree - degrees) * 60)
    seconds = round(((degree - degrees) * 60 - minutes) * 60, 2)
    return degrees, minutes, seconds

# MAISONS
# 3- Fonction pour calculer les maisons astrologiques avec les degrés totaux et DMS
def calculate_houses(jd, latitude, longitude):
    # Utiliser les mêmes fonctions de calcul que dans zodiacwheel.py
    house_cuspids, ascmc = swe.houses(jd, latitude, longitude, b'P')
    
    # Formater les résultats comme dans zodiacwheel.py
    house_results = {}
    for i, cusp in enumerate(house_cuspids):
        sign, sign_degree = get_zodiac_sign(cusp)
        degrees, minutes, seconds = convert_to_dms(cusp)  # Conversion en DMS
        
        house_results[f'Maison {i + 1}'] = {
            'degree': cusp,  # Degré total en décimal
            'sign': sign,    # Signe correspondant
            'sign_degree': sign_degree,  # Degré dans le signe
            'degree_dms': f"{degrees}°{minutes}'{seconds}''"  # Degré en DMS
        }

    # Récupérer ASC et MC comme dans zodiacwheel.py
    asc = ascmc[0]
    mc = ascmc[1]



    return house_results



# TIMEZONE
# Fonction pour obtenir la géolocalisation d'un lieu
def get_location(city, country):
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city}, {country}", timeout=10)
    
    if not location:
        return None, "Lieu de naissance introuvable."
    
    return location, None  # Retourne la localisation et None pour indiquer qu'il n'y a pas d'erreur

# Fonction pour obtenir le fuseau horaire d'une localisation
def get_timezone(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    
    if not timezone_str:
        return None, "Fuseau horaire non trouvé."
    
    return timezone_str, None  # Retourne le fuseau horaire et None pour indiquer qu'il n'y a pas d'erreur

# Fonction pour convertir une date de naissance en heures locales et UTC
def convert_birth_datetime(birth_datetime, timezone_str):
    try:
        # Conversion en heures locales
        if timezone_str == "America/Cayenne":
            timezone = pytz.timezone("Etc/GMT+3")
            birth_datetime_local = timezone.localize(birth_datetime)
        else:
            birth_datetime_local = birth_datetime.replace(tzinfo=ZoneInfo(timezone_str))
        
        # Conversion en UTC
        birth_datetime_utc = birth_datetime_local.astimezone(ZoneInfo("UTC"))

        # Retourne les dates locales et UTC sans erreur
        return birth_datetime_local, birth_datetime_utc, None

    except Exception as e:
        # En cas d'erreur, retourne None et le message d'erreur
        return None, None, f'Erreur de conversion : {e}'

# Fonction pour calculer le jour julien et les positions des planètes
def calculate_julian_day_and_planet_positions(birth_datetime_utc, latitude, longitude):
    # Calcul du jour julien (JD)
    jd = swe.julday(
        birth_datetime_utc.year,
        birth_datetime_utc.month,
        birth_datetime_utc.day,
        birth_datetime_utc.hour + birth_datetime_utc.minute / 60.0
    )
    
    # Calcul des positions des planètes
    results, planet_positions = calculate_planet_positions(jd)

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
            diff = abs(pos1 - pos2)
            diff = min(diff, 360 - diff)

            for aspect_name, aspect_angle in aspect_definitions.items():
                orbe = aspect_orbs[aspect_name]
                if abs(diff - aspect_angle) <= orbe:
                    # Ajouter l'aspect sous forme de tuple (type_aspect, pos1, pos2)
                    aspects.append((aspect_name, pos1, pos2))


    return aspects
    

# Fonction pour formater les aspects en texte lisible avec les positions et l'écart en degrés
def format_aspects_text(aspects, planet_positions):
    # Dictionnaire pour retrouver le nom de la planète à partir de la position
    planet_dict = {position: name for name, position in planet_positions}
    
    formatted_aspects = []
    for aspect_name, pos1, pos2 in aspects:
        planet1 = planet_dict.get(pos1, "Inconnu")
        planet2 = planet_dict.get(pos2, "Inconnu")
        ecart = abs(pos1 - pos2)
        ecart = min(ecart, 360 - ecart)  # Toujours l'écart le plus court entre les deux points
        
        # Formater le texte pour inclure les positions et l'écart
        formatted_aspects.append(
            f"« {aspect_name} »  {planet1} ({pos1:.2f}°) et {planet2} ({pos2:.2f}°), avec un écart de « {ecart:.2f}° »."
        )

    
    return formatted_aspects






    
# BIRTH DATA
# 6- Vue principale pour traiter les données de naissance
def birth_data(request):
    if request.method == 'POST':
        print("Débogage : La vue 'birth_data' a été appelée.")  # Vérifier si la vue est exécutée
        # Récupération des données du formulaire
        name = request.POST['name']
        date_of_birth = request.POST['date_of_birth']
        time_of_birth = request.POST['time_of_birth']
        country_of_birth = request.POST['country_of_birth']
        city_of_birth = request.POST['city_of_birth']

        # Conversion de la chaîne de texte en datetime
        birth_datetime_str = f"{date_of_birth} {time_of_birth}"
        birth_datetime = datetime.strptime(birth_datetime_str, "%Y-%m-%d %H:%M")

        # Géolocalisation du lieu de naissance
        location, error = get_location(city_of_birth, country_of_birth)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Extraction des coordonnées de latitude et longitude
        latitude = location.latitude
        longitude = location.longitude
        
        # Recherche du fuseau horaire
        timezone_str, error = get_timezone(latitude, longitude)
        if error:
            return render(request, 'birth_data_form.html', {'error': error})

        # Ajouter le timestamp pour le forçage du rechargement de l'image
        timestamp = int(now().timestamp())

        # Conversion des coordonnées en DMS (Degrés, Minutes, Secondes)
        latitude_dms = decimal_to_dms(latitude, is_latitude=True)
        longitude_dms = decimal_to_dms(longitude, is_latitude=False)


        # Conversion en heures locales et UTC
        try:
            birth_datetime_local, birth_datetime_utc, error = convert_birth_datetime(birth_datetime, timezone_str)
            if error:
                return render(request, 'birth_data_form.html', {'error': error})


            # Afficher les données d'entrée avant conversion
            print(f"Débogage : Heure de naissance d'origine (locale, avant conversion): {birth_datetime}")
            print(f"Débogage : Fuseau horaire détecté : {timezone_str}")

            # Corriger le fuseau horaire si nécessaire
            if timezone_str == "America/Cayenne":
                # Appliquer directement le fuseau horaire UTC-3 en utilisant pytz
                timezone = pytz.timezone("Etc/GMT+3")
                birth_datetime_local = timezone.localize(birth_datetime)
            else:
                birth_datetime_local = birth_datetime.replace(tzinfo=ZoneInfo(timezone_str))

            # Convertir l'heure locale en UTC
            birth_datetime_utc = birth_datetime_local.astimezone(ZoneInfo("UTC"))


            # Afficher les heures obtenues après conversion
            print(f"Débogage : Heure locale après conversion : {birth_datetime_local}")
            print(f"Débogage : Heure UTC après conversion : {birth_datetime_utc}")

        except Exception as e:
            return render(request, 'birth_data_form.html', {'error': f'Erreur de conversion : {e}'})


            
            

        # Calcul du jour julien (JD)
        jd = swe.julday(
            birth_datetime_utc.year,
            birth_datetime_utc.month,
            birth_datetime_utc.day,
            birth_datetime_utc.hour + birth_datetime_utc.minute / 60.0
        )

        # Calcul des positions des planètes
        results, planet_positions = calculate_planet_positions(jd)
        print("Débogage : Calcul des positions des planètes terminé.")  # Vérifier si les calculs sont faits

        # Calcul des maisons astrologiques
        house_results = calculate_astrological_houses(jd, latitude, longitude)
        
        # Calcul des aspects planétaires
        aspects = calculate_astrological_aspects(planet_positions)

        # Ajout de la ligne pour formater le texte des aspects, sans impacter la roue
        aspects_text = format_aspects_text(aspects, planet_positions)

        # Appel de la fonction pour générer la roue astrologique avec les aspects d'origine
        generate_astrological_wheel(planet_positions, house_results, aspects)

        # Transmission des données au modèle, avec aspects_text pour l'affichage
        return render(request, 'birth_results.html', {
            'name': name,
            'results': results,
            'houses': house_results,
            'aspects': aspects_text,  # Ici, on utilise aspects_text pour l'affichage en texte
            'local_year_str': birth_datetime_local.strftime("%Y"),
            'local_time_str': birth_datetime_local.strftime("%H:%M:%S %Z%z"),
            'utc_time_str': birth_datetime_utc.strftime("%H:%M:%S %Z%z"),
            'location': location,
            'latitude_dms': latitude_dms,
            'longitude_dms': longitude_dms,
        })


        # Appel de la fonction pour générer la roue astrologique
        print("Débogage : Appel de la fonction 'generate_astrological_wheel'.")
        generate_astrological_wheel(planet_positions, house_results, aspects)



        # Transmission des données à la template HTML
        return render(request, 'birth_results.html', {
            'name': name,
            'results': results,
            'houses': house_results,
            'aspects': aspects,
            'local_year_str': birth_datetime_local.strftime("%Y"),
            'local_time_str': birth_datetime_local.strftime("%H:%M:%S %Z%z"),
            'utc_time_str': birth_datetime_utc.strftime("%H:%M:%S %Z%z"),
            'location': location,
            'latitude_dms': latitude_dms,
            'longitude_dms': longitude_dms,
        })


    # Si la méthode n'est pas POST, afficher le formulaire de saisie
    return render(request, 'birth_data_form.html')



# PLANETES
# 7- Position des Planètes
def planetary_position(request):
    selected_date = request.GET.get('date')
    city_of_birth = request.GET.get('city_of_birth')
    country_of_birth = request.GET.get('country_of_birth')

    # Vérifier si les champs requis sont fournis
    if not selected_date or not city_of_birth or not country_of_birth:
        return HttpResponse("Tous les champs (date, ville de naissance, pays de naissance) doivent être renseignés.")

    # Convertir la date en objet datetime
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")

    # Extraire le jour, le mois et l'année pour affichage
    local_day_str = date_obj.day
    local_month_str = date_obj.strftime("%B")  # Mois sous forme de texte (ex: Janvier)
    local_year_str = date_obj.year

    # Utiliser le geolocator pour obtenir la latitude et la longitude
    print("Debug - Tentative de géolocalisation avec geolocator")
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city_of_birth}, {country_of_birth}", timeout=10)
    print(f"Debug - Résultat de la géolocalisation: {location}")

    # Vérifier si le lieu a été trouvé
    if not location:
        return HttpResponse("Lieu de naissance introuvable. Veuillez vérifier l'orthographe ou entrer un autre lieu.")

    latitude = location.latitude
    longitude = location.longitude

    # Debugging: Afficher les valeurs de latitude et longitude
    print(f"Debug - Latitude: {latitude}, Longitude: {longitude}")

    # Debug: Vérifier les valeurs de ville et pays
    print(f"Debug - Ville de naissance: {city_of_birth}, Pays de naissance: {country_of_birth}")

    # Fixer manuellement le fuseau horaire si le lieu est Cayenne
    if city_of_birth.lower() == "cayenne" and country_of_birth.lower() in ["guyane française", "french guiana"]:
        timezone_at = "Etc/GMT+3"  # Utiliser UTC-3 comme fuseau horaire manuel pour éviter les erreurs
        print("Débogage : Fuseau horaire pour Cayenne forcé à UTC-3")

    else:
        # Utiliser TimezoneFinder pour obtenir le fuseau horaire
        tf = TimezoneFinder()
        print("Debug - Création de l'objet TimezoneFinder")
        timezone_at = tf.timezone_at(lng=longitude, lat=latitude)
        print(f"Debug - Fuseau horaire détecté par TimezoneFinder : {timezone_at}")

    # Vérifier si le fuseau horaire a été trouvé
    if not timezone_at:
        return HttpResponse("Impossible de déterminer le fuseau horaire pour ce lieu.")

    # Ajuster l'heure à l'heure locale avec pytz et convertir en UTC
    try:
        local_tz = pytz.timezone(timezone_at)
        print(f"Debug - Tentative d'application du fuseau horaire détecté : {timezone_at}")
        date_obj = date_obj.replace(hour=12, minute=0)  # Utiliser l'heure d'entrée ou une valeur par défaut
        date_obj = local_tz.localize(date_obj)
        date_utc = date_obj.astimezone(pytz.utc)
        print(f"Debug - Date locale : {date_obj}, Date UTC : {date_utc}")
    except Exception as e:
        return HttpResponse(f"Erreur de conversion du fuseau horaire : {e}")

    # Calculer le jour julien (JD)
    jd = swe.julday(date_utc.year, date_utc.month, date_utc.day, date_utc.hour + date_utc.minute / 60.0)

    # Calculer les positions planétaires et les maisons
    results, planet_positions = calculate_planet_positions(jd)
    house_results = calculate_houses(jd, latitude, longitude)

    # Debugging: Afficher les résultats calculés
    print(f"Debug - Résultats des positions planétaires: {results}")

    # Retourner le rendu HTML avec les résultats
    return render(request, 'planetary_position.html', {
        'selected_date': selected_date,
        'city_of_birth': city_of_birth,
        'country_of_birth': country_of_birth,
        'local_day_str': local_day_str,
        'local_month_str': local_month_str,
        'local_year_str': local_year_str,
        'results': results,
        'houses': house_results,
    })



# TIME CONVERTION
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

def draw_segments(ax, rotation_offset):
    # Couleurs des segments par élément (feu, terre, air, eau)
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]

    # Dessiner chaque segment pour les 12 signes
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        # Calculer l'angle de début pour chaque segment
        angle = 2 * np.pi / 12 * i
        angle_corrected = angle + rotation_offset

        # Définir les angles de chaque arc en degrés
        theta1 = np.degrees(angle_corrected)
        theta2 = np.degrees(angle_corrected + 2 * np.pi / 12)

        # Dessiner l'arc extérieur pour chaque segment
        arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
        ax.add_patch(arc_outer)

        # Dessiner l'arc intérieur pour chaque segment
        arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
        ax.add_patch(arc_inner)


def draw_divisions(ax, rotation_offset):
    # Ajouter les divisions principales de 30° pour chaque signe
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        # Calculer la position corrigée de l'angle pour chaque division majeure
        angle_corrected = angle + rotation_offset
        x_outer = 1.2 * np.cos(angle_corrected)
        y_outer = 1.2 * np.sin(angle_corrected)
        x_inner = 0.8 * np.cos(angle_corrected)
        y_inner = 0.8 * np.sin(angle_corrected)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)  # Division principale de 30°

        # Ajouter les subdivisions de 5° entre chaque division principale
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            sub_angle_corrected = sub_angle + rotation_offset
            x_sub = 1.2 * np.cos(sub_angle_corrected)
            y_sub = 1.2 * np.sin(sub_angle_corrected)
            x_sub_inner = 1.1 * np.cos(sub_angle_corrected)
            y_sub_inner = 1.1 * np.sin(sub_angle_corrected)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)  # Subdivision de 5°


def draw_zodiac_symbols(ax, rotation_offset):
    # Les éléments associés aux signes du zodiaque
    elements = ['fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water']

    # Couleurs par élément
    sign_colors = {
        'fire': "#f9074c",   # Bélier, Lion, Sagittaire
        'earth': "#c59626",  # Taureau, Vierge, Capricorne
        'air': "#1a8fe9",    # Gémeaux, Balance, Verseau
        'water': "#62ce02"   # Cancer, Scorpion, Poissons
    }

    # Liste des symboles zodiacaux (en utilisant des symboles unicode ou police spécifique)
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    
    # Charger la police HamburgSymbols si nécessaire
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

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


def draw_planet_positions(ax, planet_positions, rotation_offset):
    # Symboles pour chaque planète (utilisation d'une police ou de symboles Unicode)
    planet_symbols = {
        'Soleil': 'Q', 'Lune': 'W', 'Mercure': 'E', 'Vénus': 'R', 
        'Mars': 'T', 'Jupiter': 'Y', 'Saturne': 'U', 'Uranus': 'I', 
        'Neptune': 'O', 'Pluton': 'P'
    }
    
    # Couleurs pour chaque planète
    planet_colors = {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }
    
    # Police HamburgSymbols pour les symboles planétaires
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

    # Placer chaque planète à sa position respective et ajouter les lignes de liaison
    for planet, degree in planet_positions:
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

                

def draw_houses_and_cusps(ax, house_results, rotation_offset):
    # Ajouter les lignes de cuspides pour chaque maison
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle en degrés pour chaque cuspide de maison
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Calculer la position pour la ligne de la cuspide de la maison
        x_pos = 1.27 * np.cos(angle_corrected)
        y_pos = 1.27 * np.sin(angle_corrected)
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)  # Ligne de cuspide de maison

    # Ajouter des triangles pour marquer toutes les maisons, avec des couleurs spécifiques pour les maisons principales
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle pour le triangle de la maison
        degree = house_data['degree']
        angle_corrected = np.radians(degree) + rotation_offset
        
        # Calculer la position du triangle sur la roue
        x_triangle = 1.26 * np.cos(angle_corrected)
        y_triangle = 1.26 * np.sin(angle_corrected)
        
        # Définir la couleur du triangle : noir pour les maisons principales, blanc pour les autres
        facecolor = 'black' if i + 1 in [1, 4, 7, 10] else 'white'
        
        # Ajouter le triangle avec la couleur appropriée
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05,
                                          orientation=angle_corrected + np.pi / 2,  # Orientation pour qu'il pointe vers le cercle
                                          edgecolor='black', facecolor=facecolor,
                                          linewidth=1.0, zorder=3)
        ax.add_patch(triangle)



def display_degrees(ax, planet_positions, house_results, rotation_offset):
    # Dictionnaire des couleurs des planètes
    planet_colors = {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }

    # Affichage des degrés pour chaque planète
    for planet, degree in planet_positions:
        # Calculer la position corrigée de l'angle pour les degrés de chaque planète
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        # Conversion des degrés en position dans le signe
        sign_number = int(degree // 30)  # Déterminer le signe
        degree_in_sign = degree % 30  # Degré dans le signe
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)  # Minutes dans le signe

        # Position pour les degrés de la planète
        x_degree = 1.94 * np.cos(angle_corrected)
        y_degree = 1.94 * np.sin(angle_corrected)
        
        # Position pour les minutes de la planète (plus éloigné)
        x_minutes = 2.10 * np.cos(angle_corrected)
        y_minutes = 2.10 * np.sin(angle_corrected)
        
        # Déterminer la couleur de la planète
        degree_color = planet_colors.get(planet, 'black')

        # Afficher les degrés et minutes de la planète dans la couleur correspondante
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=13, 
                ha='center', va='center', color=degree_color, weight='bold')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=11, 
                ha='center', va='center', color=degree_color, weight='bold')

    # Affichage des degrés pour chaque cuspide de maison (en noir)
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Conversion en degrés et minutes
        degree_in_sign = degree % 30  # Degré dans le signe
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)  # Minutes dans le signe

        # Position des degrés et minutes de la maison
        x_degree = 1.38 * np.cos(angle_corrected)  # Proche du cercle
        y_degree = 1.38 * np.sin(angle_corrected)
        
        x_minutes = 1.5 * np.cos(angle_corrected)  # Légèrement plus éloigné
        y_minutes = 1.5 * np.sin(angle_corrected)
        
        # Afficher les degrés et minutes de la maison en noir
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=11, 
                ha='center', va='center', color='black')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, 
                ha='center', va='center', color='black')




def draw_asc_mc_lines(ax, house_results, rotation_offset):
    # Dictionnaire pour associer ASC et MC aux maisons
    asc_mc_houses = {'ASC': 'Maison 1', 'MC': 'Maison 10'}

    # Ajouter une ligne et un marqueur pour chaque élément (ASC et MC)
    for label, house_key in asc_mc_houses.items():
        degree = house_results[house_key]['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        # Calcul des coordonnées de fin pour la ligne
        x_pos = 2.3 * np.cos(angle_corrected)
        y_pos = 2.3 * np.sin(angle_corrected)

        # Tracer la ligne du centre à la position de l'ASC ou MC
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.5, zorder=1)

        # Ajouter un triangle (flèche) pour l'ASC et un cercle pour le MC
        if label == 'ASC':
            triangle = patches.RegularPolygon((x_pos, y_pos), numVertices=3, radius=0.20,
                                              orientation=angle + rotation_offset + np.radians(270),
                                              edgecolor='black', facecolor='white', lw=0.5, zorder=3)
            ax.add_patch(triangle)

            # Placer le label "ASC"
            ax.text(x_pos + 0.4 * np.cos(angle_corrected), y_pos + 0.4 * np.sin(angle_corrected), 
                    'ASC', fontsize=12, ha='center', va='center', color='black', weight='bold')

        elif label == 'MC':
            circle = plt.Circle((x_pos, y_pos), 0.20, facecolor='white', edgecolor='black', lw=0.5, zorder=2)
            ax.add_patch(circle)

            # Placer le label "MC"
            ax.text(x_pos + 0.35 * np.cos(angle_corrected), y_pos + 0.35 * np.sin(angle_corrected), 
                    'MC', fontsize=12, ha='center', va='center', color='black', weight='bold')



def draw_house_numbers(ax, house_results, rotation_offset):
    # Dictionnaire pour convertir les numéros de maisons en chiffres romains
    roman_numerals = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }

    # Positionner chaque numéro de maison au centre de son segment
    for i in range(len(house_results)):
        # Obtenir les angles des cuspides de chaque maison
        degree_start = house_results[f'Maison {i + 1}']['degree']
        degree_end = house_results[f'Maison {(i + 2) if (i + 2) <= 12 else 1}']['degree']
        
        # Ajuster si le segment traverse 0°
        if degree_end < degree_start:
            degree_end += 360

        # Calculer l'angle médian de la maison
        degree_mid = (degree_start + degree_end) / 2
        angle_mid = np.radians(degree_mid)
        angle_mid_corrected = angle_mid + rotation_offset

        # Positionner le numéro de la maison
        x_text = 1.28 * np.cos(angle_mid_corrected)
        y_text = 1.28 * np.sin(angle_mid_corrected)
        
        # Afficher le numéro de maison au centre de chaque segment
        roman_house_num = roman_numerals[i + 1]
        ax.text(x_text, y_text, roman_house_num, fontsize=12, ha='center', va='center', color='black', weight='bold')



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
        # Obtenir le style pour le type d'aspect
        style = aspect_styles.get(type_aspect)
        if not style:
            continue  # Si le type d'aspect n'est pas défini, on ignore

        # Appliquer le décalage de rotation
        angle1 = np.radians(pos1) + rotation_offset
        angle2 = np.radians(pos2) + rotation_offset

        # Calculer les positions des extrémités des lignes d'aspect
        x1, y1 = 0.8 * np.cos(angle1), 0.8 * np.sin(angle1)  # Ajuster avec length_factor
        x2, y2 = 0.8 * np.cos(angle2), 0.8 * np.sin(angle2)

        # Dessiner la ligne d'aspect
        ax.plot([x1, x2], [y1, y2], color=style['color'], linestyle=style['linestyle'], linewidth=style['linewidth'], zorder=10)






# FIN 
def save_astrological_image(fig, image_path):
    # Supprimer l'ancienne image si elle existe
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Ancienne image supprimée : {image_path}")
    else:
        print(f"Aucune ancienne image à supprimer : {image_path}")

    # Sauvegarder la nouvelle image générée
    try:
        fig.savefig(image_path, dpi=300)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")
    finally:
        plt.close(fig)  # Fermer la figure pour libérer la mémoire

