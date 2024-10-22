import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib import font_manager
import swisseph as swe

# Dictionnaire des symboles des planètes avec la police HamburgSymbols
planet_symbols = {
    'Soleil': 'Q',  # ☉
    'Lune': 'W',    # ☽
    'Mercure': 'E', # ☿
    'Vénus': 'R',   # ♀
    'Mars': 'T',    # ♂
    'Jupiter': 'Y', # ♃
    'Saturne': 'U', # ♄
    'Uranus': 'I',  # ♅
    'Neptune': 'O', # ♆
    'Pluton': 'P'   # ♇
}

# Ajout de la définition des éléments et couleurs des planètes
elements = ['fire', 'earth', 'air', 'water', 
            'fire', 'earth', 'air', 'water', 
            'fire', 'earth', 'air', 'water']

planet_colors = {
    'Soleil': '#ffa801',
    'Lune': '#ffa801',
    'Mercure': '#a9ce02',
    'Vénus': '#bb55a1',
    'Mars': '#f9074c',
    'Jupiter': '#07b3f2',
    'Saturne': '#6a3d90',
    'Uranus': '#9B207B',
    'Neptune': '#07b3f2',
    'Pluton': '#3b2b7b'
}

def generate_wheel_image(planet_positions):
    # Charger la police HamburgSymbols
    font_path = "/mnt/c/Users/MAMAN/CALENDAR/astro/fonts/hamburgsymbols/HamburgSymbols.ttf"
    prop = font_manager.FontProperties(fname=font_path)

    # Configuration initiale avec des dimensions spécifiques
    fig, ax = plt.subplots(figsize=(18, 14))  # Grande taille pour un détail élevé
    ax.set_xlim(-1.5, 1.5)  # Ajusté pour plus de marge autour du zodiaque
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')  # Cacher les axes

    # Cercle de zodiaque avec des spécifications de couleur et style
    circle = plt.Circle((0, 0), 1.2, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(circle)

    # Couleurs et styles pour les signes du zodiaque selon les éléments
    sign_colors = {
        'fire': "#f9074c",    # Bélier, Lion, Sagittaire
        'earth': "#c59626",   # Taureau, Vierge, Capricorne
        'air': "#1a8fe9",     # Gémeaux, Balance, Verseau
        'water': "#62ce02"    # Cancer, Scorpion, Poissons
    }

    # Ajout des lignes pour chaque signe du zodiaque (30 degrés chacun)
    for i in range(12):
        angle = np.radians(30 * i)
        x = 1.2 * np.cos(angle)  # Utilisation d'un rayon légèrement supérieur
        y = 1.2 * np.sin(angle)
        ax.plot([0, x], [0, y], color=sign_colors[elements[i % 4]], linestyle='--', linewidth=1)

    # Placer les symboles des planètes avec les tailles et les couleurs originales
    for planet, degree in planet_positions:
        angle = np.radians(degree)
        x = 1.3 * np.cos(angle)  # Position un peu au-delà des signes du zodiaque
        y = 1.3 * np.sin(angle)
        symbol = planet_symbols.get(planet, "?")
        ax.text(x, y, symbol, fontdict={'fontsize': 24, 'color': planet_colors[planet], 'ha': 'center', 'va': 'center'}, fontproperties=prop)

    # Codes des signes du zodiaque pour la police HamburgSymbols
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']

    # Placer les signes du zodiaque en cercle autour de la roue
    for i, symbol in enumerate(zodiac_symbols):
        angle = np.radians(30 * i + 15)  # Centrer les signes entre les lignes
        x = 1.1 * np.cos(angle)
        y = 1.1 * np.sin(angle)
        element = elements[i % 4]  # Récupérer l'élément associé au signe
        ax.text(x, y, symbol, fontdict={'fontsize': 32, 'color': sign_colors[element], 'ha': 'center', 'va': 'center'}, fontproperties=prop)

    # Ajuster pour que la roue soit circulaire
    ax.set_aspect('equal')  # Assurer que l'aspect est égal pour éviter l'effet ovale

    # Sauvegarde du graphique en tant qu'image PNG dans le répertoire static de Django
    plt.savefig('/mnt/c/Users/MAMAN/CALENDAR/astro/staticfiles/zodiac_wheel.png')


    # Ferme la figure après avoir sauvegardé l'image
    plt.close(fig)
