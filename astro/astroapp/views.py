from timezonefinder import TimezoneFinder
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime
from django.shortcuts import render
import swisseph as swe
from zoneinfo import ZoneInfo

# 1- Fonction pour obtenir le signe astrologique à partir d'un degré
def get_zodiac_sign(degree):
    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
    ]
    sign_index = int(degree // 30)
    sign_degree = degree % 30
    return signs[sign_index], sign_degree

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

# 3- Fonction pour calculer les maisons astrologiques
# Fonction pour convertir les degrés en degrés, minutes et secondes
def convert_to_dms(degree):
    degrees = int(degree)
    minutes = int((degree - degrees) * 60)
    seconds = round(((degree - degrees) * 60 - minutes) * 60, 2)
    return degrees, minutes, seconds

# 3- Fonction pour calculer les maisons astrologiques avec les degrés totaux et DMS
# Remplacer le calcul des maisons dans views.py avec celui de zodiacwheel.py
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

    print(f"ASC: {asc}, MC: {mc}")
    print(house_results)  # Ajoute cette ligne pour afficher le contenu de house_results

    return house_results




# 4- Fonction pour convertir la date vers le fuseau horaire approprié
def convert_to_timezone(birth_datetime, timezone_str):
    tz = ZoneInfo(timezone_str)
    local_datetime = birth_datetime.replace(tzinfo=tz)
    utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
    return local_datetime, utc_datetime

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
    

# 6- Vue principale pour traiter les données de naissance
def birth_data(request):
    if request.method == 'POST':
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
        location = geolocator.geocode(f"{city_of_birth}, {country_of_birth}")

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

# 8- Vue pour afficher la roue astrologique
def wheel_view(request):
    # Calcul de la date actuelle en Julian Day
    jd = swe.julday(datetime.now().year, datetime.now().month, datetime.now().day)

    # Obtenir les positions des planètes
    _, planet_positions = calculate_planet_positions(jd)

    # Générer l'image de la roue avec les positions planétaires
    from .zodiacwheel import generate_wheel_image
    roue_zodiaque_url = generate_wheel_image(planet_positions)  # Passer l'argument ici

    return render(request, 'zodiac_wheel.html', {
        'roue_zodiaque_url': roue_zodiaque_url
    })


# 9- Fonction pour convertir les coordonnées en DMS
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

