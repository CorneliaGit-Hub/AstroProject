import os
import re

def extract_dependencies(template_dirs):
    # Stockage des dépendances par fichier
    dependencies = {}
    
    # Parcourir tous les fichiers HTML dans les répertoires des templates fournis
    for template_dir in template_dirs:
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # Stocker les dépendances pour ce fichier
                        dependencies[file] = {
                            "includes": set(),
                            "variables": set(),
                            "conditionals": set(),
                            "urls": set(),
                            "forms": set()
                        }
                        
                        # Rechercher les inclusions et statiques
                        includes = re.findall(r'{% (include|static) ["\'](.+?)["\'] %}', content)
                        dependencies[file]["includes"].update([inc[1] for inc in includes])
                        
                        # Rechercher les variables injectées
                        variables = re.findall(r'{{ (.+?) }}', content)
                        dependencies[file]["variables"].update(variables)
                        
                        # Rechercher les conditionnels et boucles, sans répétitions
                        conditionals = re.findall(r'{% if (.+?) %}', content)
                        loops = re.findall(r'{% for (.+?) in (.+?) %}', content)
                        dependencies[file]["conditionals"].update(conditionals)
                        dependencies[file]["conditionals"].update([f"{item} in {collection}" for item, collection in loops])

                        # Rechercher les liens URL
                        urls = re.findall(r'{% url ["\']?(\w+)["\']? %}', content)
                        dependencies[file]["urls"].update(urls)

                        # Rechercher les formulaires et leurs actions
                        forms = re.findall(r'<form.*?action=["\']{% url ["\']?(\w+)["\']? %}["\'].*?>', content, re.DOTALL)
                        dependencies[file]["forms"].update(forms)
    
    # Affichage formaté
    for html_file, data in dependencies.items():
        print(f"\n{html_file}")
        
        # Conditionnels et Boucles
        if data["conditionals"]:
            print("• Conditionnels et Boucles :")
            for idx, conditional in enumerate(data["conditionals"], start=1):
                if " in " in conditional:
                    print(f"{idx}. {conditional} : ")
                    print(f"{{% for {conditional} %}} ... {{% endfor %}}")
                else:
                    print(f"{idx}. {conditional} : ")
                    print(f"{{% if {conditional} %}} ... {{% endif %}}")
        
        # URLs détectées
        if data["urls"]:
            print("• URLs détectées :")
            for idx, url in enumerate(data["urls"], start=1):
                print(f"{idx}. {url} : ")
                print(f"{{% url '{url}' %}}")
        
        # Variables détectées
        if data["variables"]:
            print("• Variables détectées :")
            for idx, variable in enumerate(data["variables"], start=1):
                print(f"{idx}. {variable} : ")
                print(f"{{{{ {variable} }}}}")

        # Inclusions
        if data["includes"]:
            print("• Inclusions externes :")
            for idx, include in enumerate(data["includes"], start=1):
                print(f"{idx}. {include} : ")
                print(f"{{% include '{include}' %}}")

        # Formulaires et actions
        if data["forms"]:
            print("• Formulaires et actions :")
            for idx, form in enumerate(data["forms"], start=1):
                print(f"{idx}. {form} : ")
                print(f"<form method='post' action='{{% url '{form}' %}}'>")

# Dossiers des templates à vérifier
template_dirs = [
    "/mnt/e/CALENDAR/astro/astroapp/templates",
    "/mnt/e/CALENDAR/astro/astroapp/templates/registration"
]

# Extraction des dépendances
extract_dependencies(template_dirs)
