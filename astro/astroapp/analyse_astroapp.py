import os
import re

# Chemin du dossier de l'application
app_folder = r"/mnt/e/CALENDAR/astro/astroapp"
excluded_files = {"views_functions_variables.py", "extract_html_dependencies.py", "views.py", "analyse_astroapp.py"}

# Regex patterns pour chaque extraction spécifique
function_pattern = re.compile(r"def\s+(\w+)\s*\(.*?\):")
variable_pattern = re.compile(r"^(\w+)\s*=\s*")
admin_register_pattern = re.compile(r"admin\.site\.register\((\w+)\)")
url_pattern = re.compile(r"path\('([^']+)',\s*views\.(\w+),\s*name='([^']+)'")
model_class_pattern = re.compile(r"class\s+(\w+)\(models\.Model\):")
model_field_pattern = re.compile(r"(\w+)\s*=\s*models\.(\w+)\(.*?\)")

# Dictionnaire pour stocker les résultats
extracted_data = {}

# Parcours des fichiers Python dans le dossier
for root, _, files in os.walk(app_folder):
    for file_name in files:
        if file_name.endswith(".py") and file_name not in excluded_files:
            file_path = os.path.join(root, file_name)
            extracted_data[file_name] = {
                "functions": [],
                "variables": [],
                "admin_register": [],
                "urls": [],
                "models": {}
            }
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    current_model = None  # Suivi de la classe actuelle dans models.py
                    
                    for line in lines:
                        # Recherche de fonctions
                        if function_match := function_pattern.search(line):
                            extracted_data[file_name]["functions"].append(function_match.group(1))
                        
                        # Recherche de variables globales
                        if variable_match := variable_pattern.search(line):
                            extracted_data[file_name]["variables"].append(variable_match.group(1))
                        
                        # Recherche des enregistrements admin
                        if admin_register_match := admin_register_pattern.search(line):
                            extracted_data[file_name]["admin_register"].append(admin_register_match.group(1))
                        
                        # Recherche des chemins d'URL
                        if url_match := url_pattern.search(line):
                            extracted_data[file_name]["urls"].append({
                                "url": url_match.group(1),
                                "view": url_match.group(2),
                                "name": url_match.group(3)
                            })
                        
                        # Détection de classes de modèle
                        if model_class_match := model_class_pattern.search(line):
                            current_model = model_class_match.group(1)
                            extracted_data[file_name]["models"][current_model] = {"fields": [], "methods": []}
                        
                        # Détection des champs de modèle
                        if current_model and (field_match := model_field_pattern.search(line)):
                            extracted_data[file_name]["models"][current_model]["fields"].append((field_match.group(1), field_match.group(2)))
                        
                        # Détection des méthodes de modèle
                        if current_model and line.strip().startswith("def "):
                            method_match = function_pattern.search(line)
                            if method_match:
                                extracted_data[file_name]["models"][current_model]["methods"].append(method_match.group(1))
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_name}: {e}")

# Affichage des résultats dans la console
for file_name, data in extracted_data.items():
    print(f"\nFICHIER : {file_name}")
    
    # Fonctions
    if data["functions"]:
        print("  FONCTIONS:")
        for func_name in data["functions"]:
            print(f"    - {func_name}")
    
    # Variables
    if data["variables"]:
        print("  VARIABLES:")
        for var_name in data["variables"]:
            print(f"    - {var_name}")
    
    # Admin Registration
    if data["admin_register"]:
        print("  ENREGISTREMENTS ADMIN:")
        for model_name in data["admin_register"]:
            print(f"    - {model_name}")
    
    # URLs
    if data["urls"]:
        print("  URLS:")
        for url_info in data["urls"]:
            print(f"    - URL: {url_info['url']}, Vue: {url_info['view']}, Nom: {url_info['name']}")
    
    # Modèles
    if data["models"]:
        print("  MODÈLES:")
        for model_name, model_data in data["models"].items():
            print(f"    - Modèle: {model_name}")
            print("      Champs:")
            for field_name, field_type in model_data["fields"]:
                print(f"        - {field_name}: {field_type}")
            print("      Méthodes:")
            for method_name in model_data["methods"]:
                print(f"        - {method_name}")

