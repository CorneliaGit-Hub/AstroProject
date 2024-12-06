import os
import re

# Chemin de ton projet
project_path = "./astroapp/"  # Mets à jour ce chemin si nécessaire

# Modèles de logs trop verbeux à simplifier
patterns = [
    # Logs des planètes
    (r"logger\.debug\(f\"Planète ID .*?\"\)", ""),
    (r"logger\.debug\(f\"Résultats des positions des planètes .*?\"\)", 
     "logger.info('Calcul des positions planétaires terminé avec succès.')"),
    
    # Logs de géolocalisation
    (r"logger\.debug\(f\"Géolocalisation .*?\"\)", 
     "logger.info('Géolocalisation réussie et fuseau horaire détecté.')"),
    
    # Logs sur les images
    (r"logger\.debug\(f\"Chemin complet de l'image .*?\"\)", ""),
    (r"logger\.debug\(f\"Image supprimée .*?\"\)", 
     "logger.info('Image temporaire supprimée.')"),
]

# Parcourir tous les fichiers Python
for root, _, files in os.walk(project_path):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Appliquer les remplacements
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)

            # Sauvegarder les modifications
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

print("Tous les logs inutiles ont été supprimés ou remplacés par des messages courts.")
