import swisseph as swe
from astroapp.utils.zodiac_utils import get_zodiac_sign


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




def format_planet_positions(results, planet_positions):
    """Prépare les résultats des positions planétaires pour le retour."""
    # Affiche les résultats pour vérification
    print("Débogage : Résultats des positions des planètes ->", results)
    print("Débogage : Positions des planètes en liste ->", planet_positions)
    return results, planet_positions

