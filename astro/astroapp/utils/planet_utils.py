import numpy as np
import os
from matplotlib import font_manager
from django.conf import settings




def get_planet_data():
    """Retourne les symboles et couleurs des planètes."""
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
    
    return planet_symbols, planet_colors
    
    
    
    
def place_planet(ax, planet, degree, rotation_offset, prop, planet_symbols, planet_colors):
    """Place une planète à sa position correcte et trace la ligne de liaison."""
    # Calcul de l'angle de la planète en radians
    angle = np.radians(degree)
    angle_corrected = angle + rotation_offset
    x = 1.7 * np.cos(angle_corrected)
    y = 1.7 * np.sin(angle_corrected)
    
    # Récupérer le symbole et la couleur de la planète
    symbol = planet_symbols.get(planet, "?")
    color = planet_colors.get(planet, '#000000')  # Couleur noire par défaut si aucune correspondance

    # Ajouter le symbole de la planète avec sa couleur et sa position
    ax.text(x, y, symbol, fontproperties=prop, fontsize=40, color=color, 
            ha='center', va='center')
    
    # Tracer une ligne de liaison entre le centre et la position de la planète
    ax.plot([0, 0.9 * x], [0, 0.9 * y], color='black', lw=0.5, zorder=1)



def draw_planet_positions(ax, planet_positions, rotation_offset):
    # Appel de la fonction pour récupérer les symboles et couleurs des planètes : def get_planet_data
    planet_symbols, planet_colors = get_planet_data()

    # Police HamburgSymbols pour les symboles planétaires
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

    # Placer chaque planète à sa position respective et ajouter les lignes de liaison
    for planet, degree in planet_positions:
        
        # Appel de la fonction pour placer chaque planète : def place_planet
        place_planet(ax, planet, degree, rotation_offset, prop, planet_symbols, planet_colors)