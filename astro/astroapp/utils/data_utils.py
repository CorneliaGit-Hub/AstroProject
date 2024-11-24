import json


def format_single_aspect(aspect_name, planet1, pos1, planet2, pos2, ecart):
    """Formate un aspect individuel en texte lisible."""
    return f"« {aspect_name} »  {planet1} ({pos1:.2f}°) et {planet2} ({pos2:.2f}°), avec un écart de « {ecart:.2f}° »."


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
    
    
    
    
