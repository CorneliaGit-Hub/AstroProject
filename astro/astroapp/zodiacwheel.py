import matplotlib.pyplot as plt
import numpy as np
import os

# Définir le chemin pour l'image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_path = os.path.join(BASE_DIR, 'astroapp/static/images/zodiac_wheel.png')

# Crée la figure et les axes
fig, ax = plt.subplots()

# Crée un cercle extérieur pour la roue astrologique
outer_circle = plt.Circle((0.5, 0.5), 0.4, color='black', fill=False, linewidth=2)
ax.add_artist(outer_circle)

# Ajout d'un cercle bleu au centre
inner_circle = plt.Circle((0.5, 0.5), 0.1, color='blue', fill=True)
ax.add_artist(inner_circle)

# Ajoute 12 lignes radiales pour simuler les maisons astrologiques
for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    x = 0.5 + 0.4 * np.cos(angle)
    y = 0.5 + 0.4 * np.sin(angle)
    ax.plot([0.5, x], [0.5, y], color='black')

# Définit les limites et enlève les graduations des axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

# Assure-toi que l'image s'adapte à l'espace défini
ax.set_aspect('equal')

# Enregistre l'image dans le répertoire
plt.savefig(image_path)

# Fermer la figure pour éviter de surcharger la mémoire
plt.close(fig)

# Confirmation de la sauvegarde
if os.path.exists(image_path):
    print(f"L'image a été générée avec succès à : {image_path}")
else:
    print("Erreur : L'image n'a pas été générée.")
