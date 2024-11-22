import swisseph as swe

# JULIAN DAY 
def calculate_julian_day(birth_datetime_utc):
    """
    Calcule le jour julien (JD) à partir d'une date UTC.
    :param birth_datetime_utc: datetime en UTC
    :return: float, jour julien
    """
    return swe.julday(
        birth_datetime_utc.year,
        birth_datetime_utc.month,
        birth_datetime_utc.day,
        birth_datetime_utc.hour
        + birth_datetime_utc.minute / 60
        + birth_datetime_utc.second / 3600,
    )

def calculate_julian_day_and_planet_positions(birth_datetime_utc, latitude, longitude):

    # Appel de la fonction pour calculer le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(birth_datetime_utc)

    
    # Calcul des positions des planètes
    results, planet_positions = calculate_planet_positions(jd)

    # Ajoute ce print ici
    print("Jour Julien Calculé :", jd)
    return jd, results, planet_positions
    
def calculate_julian_and_positions(birth_datetime_utc):
    # Appel à la fonciotn qui Calcule le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(birth_datetime_utc)
    print("Débogage : Jour julien calculé ->", jd)

    # Appel à la fonciotn qui Calcule les positions des planètes : def calculate_planet_positions(jd):
    results, planet_positions = calculate_planet_positions(jd)
    print("Débogage : Calcul des positions des planètes terminé. Résultats ->", results)

    return jd, results, planet_positions
    
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


def format_planet_positions(results, planet_positions):
    """Prépare les résultats des positions planétaires pour le retour."""
    # Affiche les résultats pour vérification
    print("Débogage : Résultats des positions des planètes ->", results)
    print("Débogage : Positions des planètes en liste ->", planet_positions)
    return results, planet_positions


# Fonction pour calculer les positions des planètes
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
    
    
# ZODIAC 
# 1- Fonction pour obtenir le signe astrologique à partir d'un degré
def get_zodiac_sign(degree):
    signs = [
        "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
        "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
    ]
    sign_index = int(degree // 30)
    sign_degree = degree % 30
    return signs[sign_index], sign_degree