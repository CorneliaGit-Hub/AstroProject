from astroapp.utils.zodiac_utils import get_zodiac_sign
from astroapp.utils.conversions_utils import convert_to_dms
import swisseph as swe



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
    
    
    
# Fonction pour calculer les maisons astrologiques avec les degrés totaux et DMS
def calculate_houses(jd, latitude, longitude):
    # Appel, Utiliser les mêmes fonctions de calcul que dans zodiacwheel.py
    house_cuspids, ascmc = swe.houses(jd, latitude, longitude, b'P')
    
    # Formater les résultats comme dans zodiacwheel.py
    house_results = {}
    for i, cusp in enumerate(house_cuspids):
        # Appel de la fonction pour formater les données de la maison
        house_results[f'Maison {i + 1}'] = format_house_cusp(cusp)


    # Appel de la fonction pour obtenir l'ASC et le MC : def get_asc_mc(ascmc)
    asc, mc = get_asc_mc(ascmc)

    return house_results    
    
    
# Fonction pour calculer les maisons astrologiques
def calculate_astrological_houses(jd, latitude, longitude):
    # Utiliser les mêmes fonctions de calcul que dans zodiacwheel.py
    house_results = calculate_houses(jd, latitude, longitude)
    
    return house_results
    
    
    
# Fonction pour calculer les positions planétaires et les maisons
def calculate_positions_and_houses(jd, latitude, longitude):
    results, planet_positions = calculate_planet_positions(jd)
    house_results = calculate_houses(jd, latitude, longitude)
    
    # Debugging: Afficher les résultats calculés
    print(f"Debug - Résultats des positions planétaires: {results}")
    print(f"Debug - Résultats des maisons astrologiques: {house_results}")
    
    return results, planet_positions, house_results