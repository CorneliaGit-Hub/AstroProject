import matplotlib.pyplot as plt
import numpy as np

# Création de la figure et des axes
fig, ax = plt.subplots()

# Crée un cercle centré
circle = plt.Circle((0.5, 0.5), 0.4, color='black', fill=False)

# Ajoute le cercle aux axes
ax.add_artist(circle)

# Définit les limites des axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Enlève les graduations des axes
ax.set_xticks([])
ax.set_yticks([])

# Enregistre l'image en tant que fichier PNG dans le dossier "static/images"
plt.savefig("static/images/zodiac_wheel.png")

# Affiche le dessin
plt.show()
