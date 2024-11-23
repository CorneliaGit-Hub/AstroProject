from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pytz import timezone
from zoneinfo import ZoneInfo
from datetime import datetime




# Fonction pour obtenir la géolocalisation d'un lieu
def get_location(city, country):
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city}, {country}", timeout=10)
    
    if not location:
        return None, "Lieu de naissance introuvable."
    # Ajoute ce print ici
    print("Géolocalisation - Latitude :", location.latitude, "Longitude :", location.longitude)
    return location, None  # Retourne la localisation et None pour indiquer qu'il n'y a pas d'erreur
    

# Fonction pour obtenir le fuseau horaire d'une localisation
def get_timezone(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    
    if not timezone_str:
        return None, "Fuseau horaire non trouvé."
    
    return timezone_str, None  # Retourne le fuseau horaire et None pour indiquer qu'il n'y a pas d'erreur
    
    
def localize_datetime(birth_datetime, timezone_str):
    """Gère la localisation de birth_datetime en tenant compte du fuseau horaire spécifique."""
    if timezone_str == "America/Cayenne":
        timezone = pytz.timezone("Etc/GMT+3")
        return timezone.localize(birth_datetime)
    else:
        return birth_datetime.replace(tzinfo=ZoneInfo(timezone_str))
        
        
def extract_coordinates(location):
    """Extrait les coordonnées latitude et longitude d'un objet de localisation."""
    latitude = location.latitude
    longitude = location.longitude
    print("Débogage : Coordonnées extraites - latitude:", latitude, ", longitude:", longitude)
    return latitude, longitude


    
def retrieve_timezone(latitude, longitude):
    """Récupère le fuseau horaire pour des coordonnées données et gère les erreurs éventuelles."""
    timezone_str, error = get_timezone(latitude, longitude)
    if error:
        print("Erreur de fuseau horaire :", error)
    return timezone_str, error
    
    
    
    
def get_birth_location_data(city_of_birth, country_of_birth):
    # Géolocalisation du lieu de naissance
    location, error = get_location(city_of_birth, country_of_birth)
    if error:
        print("Erreur de géolocalisation :", error)
        return None, None, None, None, error
    
    print("Débogage : Localisation obtenue ->", location)

    # Appel de la fonction pour extraire les coordonnées latitude et longitude : def extract_coordinates
    latitude, longitude = extract_coordinates(location)

    # Appel de la fonction pour récupérer le fuseau horaire : def retrieve_timezone
    timezone_str, error = retrieve_timezone(latitude, longitude)

    
    print("Débogage : Fuseau horaire détecté ->", timezone_str)
    
    return location, latitude, longitude, timezone_str, None
    
    
 
def geolocate_city(city, country):
    """Géolocalise une ville et un pays et retourne la latitude, longitude et une erreur éventuelle."""
    geolocator = Nominatim(user_agent="astroapp")
    location = geolocator.geocode(f"{city}, {country}", timeout=10)
    if not location:
        error_message = "Lieu de naissance introuvable. Veuillez vérifier l'orthographe ou entrer un autre lieu."
        print("Erreur :", error_message)
        return None, None, error_message

    print(f"Débogage : Résultat de la géolocalisation - Latitude: {location.latitude}, Longitude: {location.longitude}")
    return location.latitude, location.longitude, None
    
    
def determine_timezone(city, country, latitude, longitude):
    """Détermine le fuseau horaire pour une ville et un pays donnés, avec un cas particulier pour Cayenne."""
    if city.lower() == "cayenne" and country.lower() in ["guyane française", "french guiana"]:
        timezone_at = "Etc/GMT+3"  # UTC-3 pour Cayenne
        print("Débogage : Fuseau horaire pour Cayenne forcé à UTC-3")
    else:
        tf = TimezoneFinder()
        timezone_at = tf.timezone_at(lng=longitude, lat=latitude)
        print(f"Debug - Fuseau horaire détecté par TimezoneFinder : {timezone_at}")

    if not timezone_at:
        error_message = "Impossible de déterminer le fuseau horaire pour ce lieu."
        print("Erreur :", error_message)
        return None, error_message

    return timezone_at, None
    
    

# Fonction pour extraire les informations de date
def extract_date_info(selected_date):
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    local_day_str = date_obj.day
    local_month_str = date_obj.strftime("%B")  # Mois sous forme de texte (ex: Janvier)
    local_year_str = date_obj.year
    print(f"Débogage : Jour -> {local_day_str}, Mois -> {local_month_str}, Année -> {local_year_str}")
    return date_obj, local_day_str, local_month_str, local_year_str