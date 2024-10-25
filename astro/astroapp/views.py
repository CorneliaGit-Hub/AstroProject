from timezonefinder import TimezoneFinder
import pytz
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
# 7- Vue pour afficher les positions planétaires
def planetary_position(request):
    selected_date = request.GET.get('date', '2024-01-01')
    city_of_birth = request.GET.get('city_of_birth', 'Paris')
    country_of_birth = request.GET.get('country_of_birth', 'France')

    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")

    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city_of_birth}, {country_of_birth}", timeout=10)

    latitude = location.latitude if location else 48.8566
    longitude = location.longitude if location else 2.3522

    delta_t = swe.deltat(date_obj.year + date_obj.month / 12.0)
    jd = swe.julday(date_obj.year, date_obj.month, date_obj.day, delta_t / 3600.0)

    results, planet_positions = calculate_planet_positions(jd)
    house_results = calculate_houses(jd, latitude, longitude)

    return render(request, 'planetary_position.html', {
        'selected_date': selected_date,
        'city_of_birth': city_of_birth,
        'country_of_birth': country_of_birth,
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
    fig, ax = plt.subplots(figsize=(8, 8))
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
        x_text = 0.96 * np.cos(angle)
        y_text = 0.96 * np.sin(angle)

        # Déterminer la couleur du signe en fonction de l'élément
        element = elements[i]
        symbol_color = sign_colors[element]

        # Définir la taille du symbole en fonction des dimensions de la figure
        symbol_size = min(fig.bbox_inches.width, fig.bbox_inches.height) * 4.2

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
        x = 1.7 * np.cos(angle)
        y = 1.7 * np.sin(angle)
        symbol = planet_symbols.get(planet, "?")
        ax.text(x, y, symbol, fontproperties=prop, fontsize=36, color=planet_colors[planet], ha='center', va='center')




# SEGMENTS
    # Couleurs des segments internes et externes pour chaque signe
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]

    # Dessiner les segments colorés pour chaque signe
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        angle = 2 * np.pi / 12 * i
        theta1 = np.degrees(angle)
        theta2 = np.degrees(angle + 2 * np.pi / 12)

        # Arc extérieur
        arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
        ax.add_patch(arc_outer)

        # Arc intérieur
        arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
        ax.add_patch(arc_inner)

    # Ajouter des divisions principales (30°) et subdivisions (5°)
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        x_outer = 1.2 * np.cos(angle)
        y_outer = 1.2 * np.sin(angle)
        x_inner = 0.8 * np.cos(angle)
        y_inner = 0.8 * np.sin(angle)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)  # Lignes des divisions principales (30°)

        # Ajouter des subdivisions (5°)
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            x_sub = 1.2 * np.cos(sub_angle)
            y_sub = 1.2 * np.sin(sub_angle)
            x_sub_inner = 1.1 * np.cos(sub_angle)
            y_sub_inner = 1.1 * np.sin(sub_angle)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)  # Lignes des subdivisions (5°)

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
    
# DEGRES    
    # --- Placer la fonction de conversion ici ---
    def convert_to_sign_degrees(degree):
        sign_number = int(degree // 30)  # Chaque signe a 30 degrés
        degree_in_sign = degree % 30  # Reste après division
        return sign_number, degree_in_sign

    # Affichage des degrés pour chaque planète
    for planet, degree in planet_positions:
        angle = np.radians(degree)
        
        # Conversion des degrés totaux en degrés du signe
        sign_number, degree_in_sign = convert_to_sign_degrees(degree)
        sign_name = zodiac_symbols[sign_number]  # Nom du signe

        # Calcul de la position pour l'affichage des degrés
        x_degree = 1.89 * np.cos(angle)  # Ajuste pour placer les degrés derrière la planète
        y_degree = 1.89 * np.sin(angle)  # Ajuste pour placer les degrés derrière la planète
        
        x_minutes = 2.05 * np.cos(angle)  # Ajuste pour placer les minutes derrière les degrés
        y_minutes = 2.05 * np.sin(angle)  # Ajuste pour placer les minutes derrière les degrés
        
        # Calcul des minutes (sans secondes)
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        # Récupérer la couleur de la planète
        degree_color = planet_colors.get(planet, '#6A3D90')  # Utiliser la couleur de la planète

        # Afficher les degrés avec la couleur de la planète
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", 
                fontsize=12, ha='center', va='center', color=degree_color, weight='bold')

        # Afficher les minutes avec la couleur de la planète, alignées derrière les degrés
        ax.text(x_minutes, y_minutes, f"{minutes}'", 
                fontsize=10, ha='center', va='center', color=degree_color, weight='bold')



        # Calcul des coordonnées pour tracer une ligne du centre à chaque planète
        x_planet = 0.0  # Centre du cercle
        y_planet = 0.0  # Centre du cercle
        x_pos = 1.5 * np.cos(angle)  # Coordonnée x de la planète sur le bord extérieur
        y_pos = 1.5 * np.sin(angle)  # Coordonnée y de la planète sur le bord extérieur

        # Tracer une ligne du centre à la position de la planète
        ax.plot([x_planet, x_pos], [y_planet, y_pos], color='black', lw=0.5, zorder=1)

    
        
    # Ajouter les cuspides des maisons
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        # Tracer une ligne pour chaque cuspide de maison
        x_pos = 1.27 * np.cos(angle)  # Coordonnée x de la cuspide de la maison
        y_pos = 1.27 * np.sin(angle)  # Coordonnée y de la cuspide de la maison
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)





    # Positionner les numéros des maisons au milieu de chaque maison
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

        # Calculer les coordonnées pour placer le texte au milieu de chaque maison
        x_text = 1.30 * np.cos(angle_mid)
        y_text = 1.30 * np.sin(angle_mid)
        
        # Afficher les numéros des maisons correctement alignés
        ax.text(x_text, y_text, f'{i + 1}', fontsize=12, ha='center', va='center', color='black')


    
    
    
    
    
    # Afficher les degrés et minutes des cuspides des maisons, convertis en degrés dans le signe
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        
        # Conversion des degrés totaux en degré dans le signe
        _, degree_in_sign = get_zodiac_sign(degree)
        degrees, minutes, _ = convert_to_dms(degree_in_sign)  # Conversion en DMS pour le degré dans le signe
        
        angle = np.radians(degree)
        
        # Position pour les degrés (plus proche du cercle)
        x_degree = 1.38 * np.cos(angle)
        y_degree = 1.38 * np.sin(angle)
        
        # Position pour les minutes (plus loin du cercle)
        x_minutes = 1.46 * np.cos(angle)
        y_minutes = 1.46 * np.sin(angle)
        
        # Afficher les degrés sans le nom du signe
        ax.text(x_degree, y_degree, f"{degrees}°", fontsize=9, ha='center', va='center', color='black')
        
        # Afficher les minutes alignés, plus loin
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, ha='center', va='center', color='black')




    # Ajouter des triangles pour marquer les cuspides des maisons
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        
        # Calculer la position des triangles sur la roue
        x_triangle = 1.26 * np.cos(angle)
        y_triangle = 1.26 * np.sin(angle)
        
        # Créer un triangle blanc avec un contour noir
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05, orientation=angle + np.pi / 2, 
                                          edgecolor='black', facecolor='white', zorder=3)
        ax.add_patch(triangle)

        # Déterminer si la cuspide est l'une des quatre maisons principales (ASC, DSC, MC, FC)
        if i + 1 in [1, 4, 7, 10]:  # Maisons 1 (ASC), 4 (FC), 7 (DSC), 10 (MC)
            facecolor = 'black'
        else:
            facecolor = 'white'

        # Créer un triangle avec la couleur appropriée
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05, orientation=angle + np.pi / 2, 
                                          edgecolor='black', facecolor=facecolor, zorder=3)
        ax.add_patch(triangle)

    
# FIN
    # Sauvegarder l'image
    try:
        plt.savefig(image_path)
        plt.close(fig)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")

