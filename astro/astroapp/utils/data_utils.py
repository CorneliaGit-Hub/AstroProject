import json
from astroapp.calculs.aspects_calculations import calculate_angular_difference
from astroapp.calculs.aspects_calculations import calculate_astrological_aspects
from astroapp.utils.planet_utils import get_planet_data  
from astroapp.utils.aspect_utils import get_aspect_data

def prepare_theme_data_json(house_results, aspects, planet_positions):
    theme_data_json = json.dumps({
        'houses': house_results,
        'aspects': aspects,
        'planet_positions': planet_positions
    })

    return theme_data_json    
    
    
    
def prepare_wheel_context(planet_positions, house_results, aspects_text):
    """Prépare le contexte pour le rendu de la roue astrologique."""
    return {
        'results': planet_positions,
        'houses': house_results,
        'aspects_text': aspects_text
    }
    
    
    
# Fonction pour préparer le contexte de rendu HTML
def prepare_planetary_context(selected_date, city_of_birth, country_of_birth, local_day_str, local_month_str, local_year_str, results, house_results):
    # Récupérer les symboles des planètes
    planet_symbols, _ = get_planet_data()
    print("DEBUG - Symboles récupérés :", planet_symbols)

    # Ajouter les symboles aux résultats (chaque planète a son symbole spécifique)
    for planet, data in results.items():
        if isinstance(data, dict):
            data['symbol'] = planet_symbols.get(planet, '?')  # Associe un symbole spécifique ou "?" par défaut
            print(f"DEBUG - {planet} : Symbole ajouté -> {data['symbol']}")
        else:
            print(f"WARNING - Données inattendues pour {planet} : {data}")

    # Retourne les données enrichies pour le template
    return {
        'selected_date': selected_date,
        'city_of_birth': city_of_birth,
        'country_of_birth': country_of_birth,
        'local_day_str': local_day_str,
        'local_month_str': local_month_str,
        'local_year_str': local_year_str,
        'results': results,
        'houses': house_results,
    }


    
    
def extract_request_parameters(request):
    """Extrait les paramètres de date, ville et pays depuis la requête GET."""
    selected_date = request.GET.get('date')
    city_of_birth = request.GET.get('city_of_birth')
    country_of_birth = request.GET.get('country_of_birth')
    return selected_date, city_of_birth, country_of_birth
    
    
    
def extract_wheel_data(request):
    """Extrait les données de la roue astrologique des paramètres GET."""
    house_results = json.loads(request.GET.get('house_results', '{}'))
    aspects = json.loads(request.GET.get('aspects', '[]'))
    planet_positions = json.loads(request.GET.get('planet_positions', '[]'))
    return house_results, aspects, planet_positions
    
    
    
def deserialize_wheel_data(house_results_str, aspects_str, planet_positions_str):
    """Désérialise les données JSON pour les maisons, les aspects et les positions planétaires."""
    try:
        house_results = json.loads(house_results_str)
        aspects = json.loads(aspects_str)
        planet_positions = json.loads(planet_positions_str)
    except json.JSONDecodeError as e:
        # Si erreur de désérialisation, initialiser avec des valeurs vides
        house_results, aspects, planet_positions = {}, [], []
        print("Erreur de désérialisation :", e)

    return house_results, aspects, planet_positions
    
    
    

def prepare_template_context(name, results, house_results, aspects, aspects_text, birth_datetime_local, birth_datetime_utc, location, latitude_dms, longitude_dms, theme_data_json):
    return {
        'name': name,
        'results': results,
        'houses': house_results,
        'aspects': aspects,
        'aspects_text': aspects_text,
        'local_day_str': birth_datetime_local.strftime("%d"),
        'local_month_str': birth_datetime_local.strftime("%B"),
        'local_year_str': birth_datetime_local.strftime("%Y"),
        'local_time_str': birth_datetime_local.strftime("%H:%M:%S %Z") + birth_datetime_local.strftime("%z")[:3],
        'utc_time_str': birth_datetime_utc.strftime("%H:%M:%S %Z") + birth_datetime_utc.strftime("%z")[:3],
        'location': location,
        'latitude_dms': latitude_dms,
        'longitude_dms': longitude_dms,
        'theme_data_json': theme_data_json
    }



def format_single_aspect(aspect_name, planet1, pos1, planet2, pos2, ecart):
    """Formate un aspect individuel en texte lisible avec symboles et couleurs."""
    # Récupération des données des aspects
    aspect_data = get_aspect_data()
    aspect_info = aspect_data.get(aspect_name, {'symbol': '', 'color': 'black'})
    aspect_symbol = aspect_info['symbol']
    aspect_color = aspect_info['color']

    # Appel à get_planet_data pour récupérer symboles et couleurs
    planet_symbols, planet_colors = get_planet_data()
    planet1_symbol = planet_symbols.get(planet1, '')
    planet2_symbol = planet_symbols.get(planet2, '')
    planet1_color = planet_colors.get(planet1, 'black')
    planet2_color = planet_colors.get(planet2, 'black')

    # Construction du texte avec style
    return f"<span class='sign-symbol' style='color: {aspect_color};'>{aspect_symbol}</span> <strong>{aspect_name} :</strong> " \
           f"<span class='planet-symbol' style='color: {planet1_color};'>{planet1_symbol}</span> <strong>{planet1}</strong> ({pos1:.2f}°) et " \
           f"<span class='planet-symbol' style='color: {planet2_color};'>{planet2_symbol}</span> <strong>{planet2}</strong> ({pos2:.2f}°), " \
           f"avec un <strong>écart</strong> de <strong>{ecart:.2f}°</strong>."



def format_aspects_text(aspects, planet_positions):
    """Formate une liste d'aspects en texte lisible."""
    # Création d'un dictionnaire position -> nom de planète
    planet_dict = {position: name for name, position in planet_positions}

    formatted_aspects = []
    for aspect_name, pos1, pos2 in aspects:
        # Récupération des noms des planètes et de leurs positions
        planet1 = planet_dict.get(pos1, "Inconnu")
        planet2 = planet_dict.get(pos2, "Inconnu")

        # Calcul de l'écart angulaire
        ecart = calculate_angular_difference(pos1, pos2)

        # Formatage de chaque aspect
        formatted_aspects.append(format_single_aspect(aspect_name, planet1, pos1, planet2, pos2, ecart))
    
    return formatted_aspects


def prepare_aspects_text(aspects, planet_positions):
    """Prépare le texte formaté des aspects pour l'affichage."""
    return format_aspects_text(aspects, planet_positions)


def generate_aspects_and_text(planet_positions):
    """Génère les aspects et leur texte formaté."""
    # Calcul des aspects planétaires
    aspects = calculate_astrological_aspects(planet_positions)

    # Formatage du texte des aspects
    aspects_text = format_aspects_text(aspects, planet_positions)

    return aspects, aspects_text

