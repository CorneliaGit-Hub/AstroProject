import swisseph as swe
from astroapp.utils.zodiac_utils import get_zodiac_sign
from astroapp.utils.zodiac_utils import get_zodiac_data  # Pour les données des signes
from astroapp.utils.planet_utils import get_planet_data  # Pour les données des planètes


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
    """
    Calcule les positions des planètes pour un jour julien donné (JD)
    et ajoute les symboles et couleurs des planètes et des signes.

    Paramètres :
    - jd : Jour julien (float).

    Retour :
    - results : Dictionnaire contenant les données des planètes (positions, symboles, couleurs).
    - planet_positions : Liste des positions des planètes pour un affichage éventuel.
    """
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

    # Récupérer les symboles et couleurs des planètes
    planet_symbols, planet_colors = get_planet_data()

    # Récupérer les symboles et couleurs des signes
    elements, sign_colors, zodiac_symbols = get_zodiac_data()

    results = {}
    planet_positions = []

    print("Débogage : Calcul des positions des planètes pour le jour julien (JD) ->", jd)

    for planet_name, planet_id in planets.items():
        # Calculer la position de chaque planète
        planet_data, planet_degree = calculate_single_planet_position(jd, planet_id)

        # Ajouter les symboles et couleurs des planètes
        planet_data['symbol'] = planet_symbols.get(planet_name, '?')
        planet_data['color'] = planet_colors.get(planet_name, '#000000')  # Noir par défaut

        # Ajouter les symboles et couleurs des signes
        sign_name = planet_data['sign']
        sign_index = [
            "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
            "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"
        ].index(sign_name)
        planet_data['sign_symbol'] = zodiac_symbols[sign_index]  # Associer le symbole du signe
        planet_data['sign_color'] = sign_colors[elements[sign_index]]  # Associer la couleur élémentaire

        print(f"DEBUG - Symbole du signe {sign_name} ajouté : {planet_data['sign_symbol']}")
        print(f"DEBUG - Couleur du signe {sign_name} ajoutée : {planet_data['sign_color']}")

        results[planet_name] = planet_data
        planet_positions.append((planet_name, planet_degree))

    # Retourner les résultats formatés
    return format_planet_positions(results, planet_positions)







def format_planet_positions(results, planet_positions):
    """Prépare les résultats des positions planétaires pour le retour."""
    # Affiche les résultats pour vérification
    print("Débogage : Résultats des positions des planètes ->", results)
    print("Débogage : Positions des planètes en liste ->", planet_positions)
    return results, planet_positions

