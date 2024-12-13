
import swisseph as swe

import astroapp.utils.swiss_ephemeris_setup

from astroapp.utils.zodiac_utils import get_zodiac_sign
from astroapp.utils.zodiac_utils import get_zodiac_data
from astroapp.utils.conversions_utils import convert_to_dms


def format_house_cusp(cusp):
    """Formate les données de la cuspide d'une maison en fonction de son degré."""
    sign, sign_degree = get_zodiac_sign(cusp)
    cusp_data = {
        'degree': cusp,  # Degré brut en décimal
        'sign': sign,
        'sign_degree': sign_degree,  # Degré dans le signe
    }
    print("Débogage - cusp_data:", cusp_data)  # Ajoutez ceci
    return cusp_data


    
    
    
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
    # Calculer les maisons
    house_results = calculate_houses(jd, latitude, longitude)
    
    # Charger les symboles et couleurs des signes
    elements, sign_colors, zodiac_symbols = get_zodiac_data()

    # Enrichir chaque maison avec les données des signes
    for house, cusp_data in house_results.items():
        cusp_degree = cusp_data['degree']  # Degré total de la cuspide
        sign, sign_degree = get_zodiac_sign(cusp_degree)  # Obtenir le signe et le degré
        sign_index = int(cusp_degree // 30)  # Index du signe

        # Ajouter les symboles et couleurs des signes
        cusp_data['sign'] = sign
        cusp_data['sign_degree'] = sign_degree
        cusp_data['sign_symbol'] = zodiac_symbols[sign_index]
        cusp_data['sign_color'] = sign_colors[elements[sign_index]]

    return house_results

    
    
    
# Fonction pour calculer les positions planétaires et les maisons
def calculate_positions_and_houses(jd, latitude, longitude):
    results, planet_positions = calculate_planet_positions(jd)
    house_results = calculate_houses(jd, latitude, longitude)
    
    # Debugging: Afficher les résultats calculés
    print(f"Debug - Résultats des positions planétaires: {results}")
    print(f"Debug - Résultats des maisons astrologiques: {house_results}")
    
    return results, planet_positions, house_results