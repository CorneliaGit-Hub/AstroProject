from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pytz import timezone
from zoneinfo import ZoneInfo
from datetime import datetime
import pytz





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
    """
    Obtenir les données de localisation et fuseau horaire d'un lieu de naissance.

    Args:
        city_of_birth (str): Nom de la ville de naissance.
        country_of_birth (str): Nom du pays de naissance.

    Returns:
        tuple: (localisation, latitude, longitude, fuseau horaire, message d'erreur).
    """
    # Géolocalisation du lieu de naissance
    location, error = get_location(city_of_birth, country_of_birth)
    if error:
        print("Erreur de géolocalisation :", error)
        return None, None, None, None, error
    
    print("Débogage : Localisation obtenue ->", location)

    # Appel de la fonction pour extraire les coordonnées latitude et longitude
    latitude, longitude = extract_coordinates(location)

    # Appel de la fonction pour récupérer le fuseau horaire
    timezone_str, error = determine_timezone(city_of_birth, country_of_birth, latitude, longitude)
    if error:
        print("Erreur lors de la détermination du fuseau horaire :", error)
        return None, None, None, None, error

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
    """
    Détermine le fuseau horaire pour un lieu donné.

    Args:
        city (str): Nom de la ville.
        country (str): Nom du pays.
        latitude (float): Latitude du lieu.
        longitude (float): Longitude du lieu.

    Returns:
        tuple: (fuseau horaire (str), message d'erreur (None si tout va bien)).
    """
    try:
        # Gestion spécifique de la Guyane française
        if country.lower() in ["guyane française", "french guiana"]:
            print("Débogage : Fuseau horaire pour la Guyane française détecté (UTC-3).")
            return "Etc/GMT+3", None

        # Sinon, détecter automatiquement le fuseau horaire
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if not timezone:
            return None, "Impossible de déterminer le fuseau horaire."

        print(f"Débogage : Fuseau horaire détecté automatiquement -> {timezone}")
        return timezone, None
    except Exception as e:
        return None, f"Erreur lors de la détermination du fuseau horaire : {e}"

    
    

# Fonction pour extraire les informations de date
def extract_date_info(selected_date):
    date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    local_day_str = date_obj.day
    local_month_str = date_obj.strftime("%B")  # Mois sous forme de texte (ex: Janvier)
    local_year_str = date_obj.year
    print(f"Débogage : Jour -> {local_day_str}, Mois -> {local_month_str}, Année -> {local_year_str}")
    return date_obj, local_day_str, local_month_str, local_year_str