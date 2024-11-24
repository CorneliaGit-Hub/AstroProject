import numpy as np
from astroapp.utils.zodiac_utils import get_zodiac_data, load_zodiac_font

def draw_zodiac_symbols(ax, rotation_offset):
    # Appel de la fonciton pour associer les éléments aux signes du zodiaque : def get_zodiac_data
    elements, sign_colors, zodiac_symbols = get_zodiac_data()


    # Liste des symboles zodiacaux (en utilisant des symboles unicode ou police spécifique)
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    
    # Appel de la fonciton pour Charger la police HamburgSymbols si nécessaire : def load_zodiac_font
    prop = load_zodiac_font()


    # Placer chaque symbole du zodiaque
    for i, symbol in enumerate(zodiac_symbols):
        # Calculer l'angle de positionnement pour chaque signe
        angle = np.radians(30 * i + 15)
        angle_corrected = angle + rotation_offset
        x_text = 0.96 * np.cos(angle_corrected)
        y_text = 0.96 * np.sin(angle_corrected)

        # Déterminer la couleur du signe en fonction de son élément
        element = elements[i]
        symbol_color = sign_colors[element]

        # Définir la taille du symbole zodiacal en fonction de la figure
        symbol_size = 40  # Ajustable si nécessaire

        # Ajouter le symbole à la figure
        ax.text(x_text, y_text, symbol, fontsize=symbol_size, 
                ha='center', va='center', fontproperties=prop, color=symbol_color)




def get_planet_colors():
    """Retourne le dictionnaire des couleurs pour chaque planète."""
    return {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }
    
    
def display_planet_degrees(ax, planet_positions, rotation_offset, planet_colors):
    """Affiche les degrés et minutes pour chaque planète sur la roue astrologique."""
    for planet, degree in planet_positions:
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        degree_in_sign = degree % 30
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        x_degree = 1.94 * np.cos(angle_corrected)
        y_degree = 1.94 * np.sin(angle_corrected)
        
        x_minutes = 2.10 * np.cos(angle_corrected)
        y_minutes = 2.10 * np.sin(angle_corrected)
        
        degree_color = planet_colors.get(planet, 'black')

        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=13, 
                ha='center', va='center', color=degree_color, weight='bold')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=11, 
                ha='center', va='center', color=degree_color, weight='bold')
    
    
    


