
def stocker_donnees_session(request, data):
    """
    Stocke les données fournies dans la session Django.
    Args:
        request: La requête HTTP.
        data: Un dictionnaire contenant les données à stocker.
    """
    for key, value in data.items():
        request.session[key] = value
    print("Données stockées en session :", request.session.items())  # Vérification dans la console
    
    
    
def extract_form_data(request):
    """
    Extrait les données du formulaire POST pour les stocker.
    Args:
        request: La requête HTTP contenant les données du formulaire.
    Returns:
        Un dictionnaire avec les données extraites ou une valeur par défaut si elles sont absentes.
    """
    return {
        "name": request.POST.get("name", "Non défini"),
        "birthdate": request.POST.get("birthdate", "Non défini"),
        "birthtime": request.POST.get("birthtime", "Non défini"),
        "country_of_birth": request.POST.get("country_of_birth", "Non défini"),
        "city_of_birth": request.POST.get("city_of_birth", "Non défini"),
    }
    
    
    
def extract_birth_data_form(request):
    name = request.POST['name']
    birthdate = request.POST['birthdate']
    birthtime = request.POST['birthtime']
    country_of_birth = request.POST['country_of_birth']
    city_of_birth = request.POST['city_of_birth']
    print("Débogage : Variables extraites - name:", name, ", birthdate:", birthdate, ", birthtime:", birthtime)
    print("Débogage : Localisation - ville:", city_of_birth, ", pays:", country_of_birth)
    return name, birthdate, birthtime, country_of_birth, city_of_birth