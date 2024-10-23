import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import numpy as np
import swisseph as swe
from matplotlib import font_manager

# Définir le chemin pour l'image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_path = os.path.join(BASE_DIR, 'astroapp/static/images/zodiac_wheel.png')

# Fonction pour calculer les positions des planètes
def calculate_planet_positions(year, month, day, hour):
    swe.set_ephe_path('/path/to/ephemeris/')  # Remplace par le chemin vers tes fichiers d'éphémérides
    julian_day = swe.julday(year, month, day, hour)

    planet_positions = {}
    planets = {
        'Soleil': swe.SUN, 'Lune': swe.MOON, 'Mercure': swe.MERCURY, 'Vénus': swe.VENUS,
        'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturne': swe.SATURN,
        'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluton': swe.PLUTO
    }
    
    for planet_name, planet_id in planets.items():
        pos, _ = swe.calc_ut(julian_day, planet_id)
        planet_positions[planet_name] = pos[0]  # Longitude
    
    return planet_positions

# Fonction pour ajouter les positions des planètes sur la roue
def add_planet_positions(ax, planet_positions, prop):  # Ajoute 'prop' comme paramètre
    planet_symbols = {
        'Soleil': 'Q', 'Lune': 'W', 'Mercure': 'E', 'Vénus': 'R', 
        'Mars': 'T', 'Jupiter': 'Y', 'Saturne': 'U', 'Uranus': 'I', 
        'Neptune': 'O', 'Pluton': 'P'
    }
    
    planet_colors = {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }
    
    for planet, degree in planet_positions.items():
        angle = np.radians(degree)
        x = 1.3 * np.cos(angle)
        y = 1.3 * np.sin(angle)
        symbol = planet_symbols.get(planet, "?")
        ax.text(x, y, symbol, fontproperties=prop, fontsize=24, color=planet_colors[planet], ha='center', va='center')

# Fonction pour créer la base de la roue astrologique
def draw_base_wheel(year, month, day, hour):
    # Création de la figure et des axes
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    # Dessiner le cercle principal
    circle = plt.Circle((0, 0), 1.2, edgecolor='black', facecolor='none', linewidth=2)
    ax.add_patch(circle)

    # Ajouter des lignes pour chaque signe
    for i in range(12):
        angle = np.radians(30 * i)
        x = 1.2 * np.cos(angle)
        y = 1.2 * np.sin(angle)
        ax.plot([0, x], [0, y], color='black', linestyle='--', linewidth=1)

    # Charger la police HamburgSymbols
    font_path = os.path.join(BASE_DIR, 'astroapp/fonts/hamburgsymbols/HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

    # Ajouter les symboles des signes du zodiaque
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    for i, symbol in enumerate(zodiac_symbols):
        angle = np.radians(30 * i + 15)
        x = 1.1 * np.cos(angle)
        y = 1.1 * np.sin(angle)
        ax.text(x, y, symbol, fontproperties=prop, fontsize=24, ha='center', va='center')

    # Calculer et ajouter les positions des planètes
    planet_positions = calculate_planet_positions(year, month, day, hour)
    add_planet_positions(ax, planet_positions, prop)  # Passe 'prop' ici

# FIN
    # Enregistrer l'image
    plt.savefig(image_path)
    plt.close(fig)

    # Confirmation de la sauvegarde
    if os.path.exists(image_path):
        print(f"L'image a été générée avec succès à : {image_path}")
    else:
        print("Erreur : L'image n'a pas été générée.")

# Appeler la fonction pour tester avec une date
if __name__ == "__main__":
    draw_base_wheel(1966, 10, 28, 04.05)
