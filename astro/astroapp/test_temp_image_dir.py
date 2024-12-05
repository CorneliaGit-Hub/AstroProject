import os
import sys
import django
from django.conf import settings

# Ajouter le dossier racine au chemin des modules Python
sys.path.append('/mnt/e/CALENDAR/astro')

# Initialiser Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroconfig.settings')
django.setup()

# Tester TEMP_IMAGE_DIR
user_id = 349
image_name = "test_chart.png"
image_path = os.path.join(settings.TEMP_IMAGE_DIR, str(user_id), image_name)

# Créer le répertoire utilisateur
os.makedirs(os.path.dirname(image_path), exist_ok=True)

# Exemple d'impression
print("Chemin d'image généré :", image_path)
