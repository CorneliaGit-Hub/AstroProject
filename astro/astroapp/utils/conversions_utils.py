from zoneinfo import ZoneInfo
from astroapp.utils.geolocation_utils import localize_datetime
from datetime import datetime
from django.utils.timezone import now


# Fonction pour convertir les degrés en degrés, minutes et secondes
def convert_to_dms(degree):
    degrees = int(degree)
    minutes = int((degree - degrees) * 60)
    seconds = round(((degree - degrees) * 60 - minutes) * 60, 2)
    return degrees, minutes, seconds


def convert_to_utc(local_datetime):
    """Convertit un datetime localisé en heure UTC."""
    return local_datetime.astimezone(ZoneInfo("UTC"))
    
    

# Fonction pour convertir une date de naissance en heures locales et UTC
def convert_birth_datetime(birth_datetime, timezone_str):
    try:
        # Appel de la fonction pour convertir en heure locale :  def localize_datetime
        birth_datetime_local = localize_datetime(birth_datetime, timezone_str)
        
        # Appel de la fonction pour convertir l'heure locale en UTC : def convert_to_utc
        birth_datetime_utc = convert_to_utc(birth_datetime_local)  # Enlever timezone_str
        error = None  # Pas d'erreur à gérer


        # Si une erreur est détectée, retourne l'erreur
        if error:
            return None, None, error
            
        # Ajoute ces prints ici
        print("Fuseau Horaire :", timezone_str)
        print("Date/Heure UTC :", birth_datetime_utc)
    
        # Retourne les dates locales et UTC sans erreur
        return birth_datetime_local, birth_datetime_utc, None

    except Exception as e:
        # En cas d'erreur, retourne None et le message d'erreur
        return None, None, f'Erreur de conversion : {e}'



def convert_latlon_to_dms(latitude, longitude):
    # Conversion des coordonnées en DMS (Degrés, Minutes, Secondes)
    latitude_dms = decimal_to_dms(latitude, is_latitude=True)
    longitude_dms = decimal_to_dms(longitude, is_latitude=False)
    print("Débogage : Coordonnées en DMS - latitude_dms:", latitude_dms, ", longitude_dms:", longitude_dms)
    return latitude_dms, longitude_dms
    
    
# Fonction pour convertir les coordonnées en DMS
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
    
    
    
def convert_to_local_and_utc(birth_datetime, timezone_str):
    """Convertit une date de naissance en heures locales et UTC."""
    birth_datetime_local, birth_datetime_utc, error = convert_birth_datetime(birth_datetime, timezone_str)
    if error:
        print("Erreur de conversion datetime :", error)
        return None, None, error

    print("Débogage : Conversion datetime réussie - Heure locale :", birth_datetime_local, ", Heure UTC :", birth_datetime_utc)
    return birth_datetime_local, birth_datetime_utc, None
    
    


def create_birth_datetime_and_timestamp(birthdate, birthtime):
    birth_datetime_str = f"{birthdate} {birthtime}"
    # Supporte les formats avec ou sans secondes
    try:
        birth_datetime = datetime.strptime(birth_datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        birth_datetime = datetime.strptime(birth_datetime_str, "%Y-%m-%d %H:%M")


    print("Débogage : birth_datetime construit ->", birth_datetime)

    # Création du timestamp pour rechargement de l'image
    timestamp = int(now().timestamp())
    print("Débogage : Timestamp ajouté ->", timestamp)
    
    return birth_datetime, timestamp
    
    
 

def convert_coordinates_to_dms(latitude, longitude):
    latitude_dms, longitude_dms = convert_latlon_to_dms(latitude, longitude)
    return latitude_dms, longitude_dms

    
