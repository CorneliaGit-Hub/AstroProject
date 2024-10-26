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
# 4- Fonction pour convertir la date vers le fuseau horaire approprié
def convert_to_timezone(birth_datetime, timezone_str):
    tz = ZoneInfo(timezone_str)
    local_datetime = birth_datetime.replace(tzinfo=tz)
    utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
    return local_datetime, utc_datetime


# ASPECTS
# 5- Fonction pour afficher les aspects planétaires
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
                    aspects.append(f"{planet1} - {planet2}: {aspect_name}")

    return aspects
    
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
        geolocator = Nominatim(user_agent="astroapp")
        location = geolocator.geocode(f"{city_of_birth}, {country_of_birth}", timeout=10)

        if not location:
            return render(request, 'birth_data_form.html', {'error': 'Lieu de naissance introuvable.'})

        # Récupérer les coordonnées de latitude et longitude
        latitude = location.latitude
        longitude = location.longitude

        # Conversion des coordonnées en DMS (Degrés, Minutes, Secondes)
        latitude_dms = decimal_to_dms(latitude, is_latitude=True)
        longitude_dms = decimal_to_dms(longitude, is_latitude=False)

        # Recherche du fuseau horaire
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=longitude, lat=latitude)

        if not timezone_str:
            return render(request, 'birth_data_form.html', {'error': 'Fuseau horaire non trouvé.'})

        # Conversion en heures locales et UTC
        try:
            birth_datetime_local, birth_datetime_utc = convert_to_timezone(birth_datetime, timezone_str)

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

        # Calcul des positions des planètes et des maisons astrologiques
        results, planet_positions = calculate_planet_positions(jd)
        house_results = calculate_houses(jd, latitude, longitude)

        print("Débogage : Calcul des positions des planètes terminé.")  # Vérifier si les calculs sont faits

        # Appel de la fonction pour générer la roue astrologique
        print("Débogage : Appel de la fonction 'generate_astrological_wheel'.")
        generate_astrological_wheel(planet_positions, house_results)

        # Calcul des aspects planétaires
        aspects = calculate_aspects(planet_positions)

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
# 9-Génération de la roue astrologique avec les données calculées
def generate_astrological_wheel(planet_positions, house_results):
    # Calcul de l'offset de rotation pour positionner l'ASC toujours à gauche
    asc_angle = house_results['Maison 1']['degree']
    rotation_offset = np.radians(-asc_angle + 180)

    # Chemin pour l'image
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(BASE_DIR, 'astroapp/static/images/zodiac_wheel.png') 

    # Supprimer l'image précédente si elle existe
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Ancienne image supprimée : {image_path}")
    else:
        print(f"Aucune ancienne image à supprimer : {image_path}")

    # Créer la figure et les axes pour la roue astrologique
    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')

    # Dessiner le cercle principal
    circle = plt.Circle((0, 0), 1.2, edgecolor='black', facecolor='none', linewidth=1)
    ax.add_patch(circle)

    # Charger la police HamburgSymbols
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

        
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

    # Ajouter les signes astrologiques avec la couleur selon l'élément
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    for i, symbol in enumerate(zodiac_symbols):
        angle = np.radians(30 * i + 15)
        angle_corrected = angle + rotation_offset
        x_text = 0.96 * np.cos(angle_corrected)
        y_text = 0.96 * np.sin(angle_corrected)

        # Déterminer la couleur du signe en fonction de l'élément
        element = elements[i]
        symbol_color = sign_colors[element]

        # Définir la taille du SIGNES en fonction des dimensions de la figure
        symbol_size = min(fig.bbox_inches.width, fig.bbox_inches.height) * 2.5  # Taille des signes

        # Ajouter le symbole avec la couleur et la taille correspondantes
        ax.text(x_text, y_text, symbol, fontsize=symbol_size, 
                ha='center', va='center', fontproperties=prop, color=symbol_color)


# PLANETES
    # Ajouter les positions des planètes (en fonction de `planet_positions`)
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

    for planet, degree in planet_positions:
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        x = 1.7 * np.cos(angle_corrected)
        y = 1.7 * np.sin(angle_corrected)
        symbol = planet_symbols.get(planet, "?")
        ax.text(x, y, symbol, fontproperties=prop, fontsize=40, color=planet_colors[planet], ha='center', va='center') # Taille des Planètes




# SEGMENTS
    # Couleurs des segments internes et externes pour chaque signe
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]

    # Dessiner les segments colorés pour chaque signe
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        angle = 2 * np.pi / 12 * i
        angle_corrected = angle + rotation_offset  # Appliquer le décalage pour chaque segment

        theta1 = np.degrees(angle_corrected)
        theta2 = np.degrees(angle_corrected + 2 * np.pi / 12)

        # Arc extérieur
        arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
        ax.add_patch(arc_outer)

        # Arc intérieur
        arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
        ax.add_patch(arc_inner)


    # Ajouter des divisions principales (30°) 
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        angle_corrected = angle + rotation_offset
        x_outer = 1.2 * np.cos(angle_corrected)
        y_outer = 1.2 * np.sin(angle_corrected)
        x_inner = 0.8 * np.cos(angle_corrected)
        y_inner = 0.8 * np.sin(angle_corrected)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)  # Lignes des divisions principales (30°)

        # Ajouter des subdivisions (5°)
        # Ici on doit ajuster la logique pour qu'elle corrige toutes les subdivisions, pas seulement la première boucle
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            sub_angle_corrected = sub_angle + rotation_offset
            x_sub = 1.2 * np.cos(sub_angle_corrected)
            y_sub = 1.2 * np.sin(sub_angle_corrected)
            x_sub_inner = 1.1 * np.cos(sub_angle_corrected)
            y_sub_inner = 1.1 * np.sin(sub_angle_corrected)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)  # Lignes des subdivisions (5°)

        
        
        
# CERCLE BLANC
    # Ajouter un cercle blanc au centre après les autres éléments
    circle_inner_white = plt.Circle((0, 0), 0.80, color='white', ec='black', linewidth=0.5, zorder=10) # Largeur du diamètre, le nombre après les parenthèses
    ax.add_patch(circle_inner_white)

    # Ajouter un cercle extérieur noir pour la bordure
    circle_outer_border = plt.Circle((0, 0), 1.2, color='none', ec='black', linewidth=0.5, zorder=5)
    ax.add_patch(circle_outer_border)

    # Ajuster les Marges de l'image
    plt.subplots_adjust(left=0.1, right=0.9, top=0.87, bottom=0.14)  # Ajuste ces valeurs selon tes besoins

    # Limiter l'affichage 
    ax.set_xlim(-1.5, 1.5)  # Ajustement selon la taille des éléments
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
# PLANETES    
    # --- Placer la fonction de conversion ici ---
    def convert_to_sign_degrees(degree):
        sign_number = int(degree // 30)  # Chaque signe a 30 degrés
        degree_in_sign = degree % 30  # Reste après division
        return sign_number, degree_in_sign

    # Affichage des degrés pour chaque planète
    for planet, degree in planet_positions:
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Conversion des degrés totaux en degrés du signe
        sign_number, degree_in_sign = convert_to_sign_degrees(degree)
        sign_name = zodiac_symbols[sign_number]  # Nom du signe

        # Calcul de la position pour l'affichage des degrés
        x_degree = 1.94 * np.cos(angle_corrected)  # Déplacement du Degrés des Planètes
        y_degree = 1.94 * np.sin(angle_corrected)  # Déplacement du Degrés des Planètes
        
        x_minutes = 2.10 * np.cos(angle_corrected)  # Déplacement des minutes
        y_minutes = 2.10 * np.sin(angle_corrected)  # Déplacement des minutes

        
        # Calcul des minutes (sans secondes)
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        # Récupérer la couleur de la planète
        degree_color = planet_colors.get(planet, '#6A3D90')  # Utiliser la couleur de la planète

        # Afficher les degrés avec la couleur de la planète
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", 
                fontsize=13, ha='center', va='center', color=degree_color, weight='bold') # Taille des Degrés des Planètes

        # Afficher les minutes avec la couleur de la planète, alignées derrière les degrés
        ax.text(x_minutes, y_minutes, f"{minutes}'", 
                fontsize=11, ha='center', va='center', color=degree_color, weight='bold') # Taille des Degrés des Planètes


        # Calcul des coordonnées pour tracer une ligne du centre à chaque planète
        x_planet = 0.0  # Centre du cercle
        y_planet = 0.0  # Centre du cercle
        angle_corrected = angle + rotation_offset
        x_pos = 1.5 * np.cos(angle_corrected)  # Coordonnée x de la planète sur le bord extérieur
        y_pos = 1.5 * np.sin(angle_corrected)  # Coordonnée y de la planète sur le bord extérieur

        # Tracer une ligne du centre à la position de la planète
        ax.plot([x_planet, x_pos], [y_planet, y_pos], color='black', lw=0.5, zorder=1)

    
# MAISONS      
    # Ajouter les cuspides des maisons
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        # Tracer une ligne pour chaque cuspide de maison
        x_pos = 1.27 * np.cos(angle_corrected)  # Coordonnée x de la cuspide de la maison
        y_pos = 1.27 * np.sin(angle_corrected)  # Coordonnée y de la cuspide de la maison
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)

        
        

    # Dictionnaire pour convertir les numéros en chiffres romains
    roman_numerals = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }

    # Positionner les numéros des maisons au milieu de chaque maison en chiffres romains
    for i in range(len(house_results)):
        # Calculer les angles de départ et de fin pour chaque maison
        degree_start = house_results[f'Maison {i + 1}']['degree']
        degree_end = house_results[f'Maison {(i + 2) if (i + 2) <= 12 else 1}']['degree']
        
        # S'assurer que les maisons ne sont pas inversées ou mal positionnées
        if degree_end < degree_start:
            degree_end += 360  # Ajouter 360 degrés si la cuspide traverse 0°

        # Calculer l'angle médian entre deux cuspides
        degree_mid = (degree_start + degree_end) / 2
        angle_mid = np.radians(degree_mid)

        # Calculer les coordonnées pour placer les Numéros au milieu de chaque maison
        angle_mid_corrected = angle_mid + rotation_offset
        x_text = 1.28 * np.cos(angle_mid_corrected)
        y_text = 1.28 * np.sin(angle_mid_corrected)

        
        # Utiliser le dictionnaire pour afficher les chiffres romains
        roman_house_num = roman_numerals[i + 1]  # Récupérer le chiffre romain
        ax.text(x_text, y_text, roman_house_num, fontsize=12, ha='center', va='center', color='black', weight='bold')  # Taille des numéros des Maisons

        
        
        
        
        
    
    # Afficher les degrés et minutes des cuspides des maisons, convertis en degrés dans le signe
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        
        # Conversion des degrés totaux en degré dans le signe
        _, degree_in_sign = get_zodiac_sign(degree)
        degrees, minutes, _ = convert_to_dms(degree_in_sign)  # Conversion en DMS pour le degré dans le signe
        
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Position pour les degrés (plus proche du cercle)
        x_degree = 1.38 * np.cos(angle_corrected)  # Déplacement du Degrés des Maisons
        y_degree = 1.38 * np.sin(angle_corrected)  # Déplacement du Degrés des Maisons
        
        # Position pour les minutes (plus loin du cercle)
        x_minutes = 1.5 * np.cos(angle_corrected)  # Déplacement du Minutes des Maisons
        y_minutes = 1.5 * np.sin(angle_corrected)  # Déplacement du Minutes des Maisons
        
        # Afficher les degrés sans le nom du signe
        ax.text(x_degree, y_degree, f"{degrees}°", fontsize=11, ha='center', va='center', color='black') # Taille des Degrés des Maisons
        
        # Afficher les minutes alignés, plus loin
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, ha='center', va='center', color='black') # Taille des Minutes des Maisons




    # Ajouter des Triangles pour marquer les cuspides des maisons
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle_corrected = np.radians(degree) + rotation_offset
        
        # Calculer la position des triangles sur la roue
        x_triangle = 1.26 * np.cos(angle_corrected)
        y_triangle = 1.26 * np.sin(angle_corrected)
        
        # Déterminer la couleur en fonction de la maison (noir pour les maisons 1, 4, 7, 10)
        facecolor = 'black' if i + 1 in [1, 4, 7, 10] else 'white'
        
        # Créer un seul triangle avec la couleur appropriée
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05,
                                          orientation=angle_corrected + np.pi / 2,  # Ajustement de l'orientation
                                          edgecolor='black', facecolor=facecolor,
                                          linewidth=1.0, zorder=3)
        ax.add_patch(triangle)



        
        
        

    # Ajouter les lignes pour l'ASC et le MC avec flèche (triangle) et cercle
    for i, house in enumerate(['ASC', 'MC']):
        if house == 'ASC':  # ASC correspond à la maison 1
            degree = house_results['Maison 1']['degree']
        elif house == 'MC':  # MC correspond à la maison 10
            degree = house_results['Maison 10']['degree']
        
        # Calculer l'angle de la ligne
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Calculer les coordonnées de fin pour la ligne (même que pour les planètes)
        x_pos = 2.3 * np.cos(angle_corrected)
        y_pos = 2.3 * np.sin(angle_corrected)

        
        # Tracer la ligne depuis le centre jusqu'à la position calculée
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.5, zorder=1)
        
        
        
        
        # Ajouter un triangle (flèche) pour l'ASC et un cercle pour le MC
        if house == 'ASC':
            # Appliquer une orientation qui contrebalance le rotation_offset pour que la flèche pointe toujours vers la gauche
            triangle = patches.RegularPolygon((x_pos, y_pos), numVertices=3, radius=0.20,
                                              orientation=angle + rotation_offset + np.radians(270),  # Décalé pour pointer à gauche
                                              edgecolor='black', facecolor='white', lw=0.5, zorder=3)
            ax.add_patch(triangle)

            # Ajouter le label "ASC" plus vers l'extérieur avec rotation_offset
            angle_corrected = angle + rotation_offset
            ax.text(x_pos + 0.4 * np.cos(angle_corrected), y_pos + 0.4 * np.sin(angle_corrected), 'ASC', fontsize=12, 
                    ha='center', va='center', color='black', weight='bold')




        elif house == 'MC':
            # Ajouter un cercle blanc avec un contour noir
            circle = plt.Circle((x_pos, y_pos), 0.20, facecolor='white', edgecolor='black', lw=0.5, zorder=2)
            ax.add_patch(circle)


            # Ajouter le label "MC" plus vers l'extérieur
            angle_corrected = angle + rotation_offset
            ax.text(x_pos + 0.35 * np.cos(angle_corrected), y_pos + 0.35 * np.sin(angle_corrected), 'MC', fontsize=12, 
                    ha='center', va='center', color='black', weight='bold')










        # Ajuster les limites de l'axe sans couper les angles
        ax.set_xlim(-2.9, 2.9)
        ax.set_ylim(-2.9, 2.9)

        # Supprimer les marges automatiques autour de la figure
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Régler les proportions de la figure pour qu'elle soit carrée et occupe tout l'espace
        fig.set_size_inches(12, 12)
        ax.set_aspect('equal')






            
# FIN
    # Sauvegarder l'image
    try:
        plt.savefig(image_path, dpi=300)
        plt.close(fig)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")


