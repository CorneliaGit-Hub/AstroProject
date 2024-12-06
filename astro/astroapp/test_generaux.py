import os
import re

# Chemin du dossier contenant les fichiers à modifier
directory = "./astroapp/"

# Parcourir tous les fichiers dans le dossier
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):  # Modifier uniquement les fichiers Python
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remplacer les print par logger.debug
            # Exemple : print("Message :", variable) -> logger.debug(f"Message : {variable}")
            new_content = re.sub(
                r'print\((.*)\)',
                r'logger.debug(f"\1")',
                content
            )

            # Ajouter l'import du logger si nécessaire
            if "import logging" not in new_content:
                new_content = "import logging\nlogger = logging.getLogger('astroapp')\n\n" + new_content

            # Écrire les modifications dans le fichier
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

print("Les fichiers ont été modifiés avec succès !")
