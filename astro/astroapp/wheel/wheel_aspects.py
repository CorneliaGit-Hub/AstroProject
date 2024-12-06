import numpy as np


def get_aspect_style(type_aspect):
    """Retourne le style pour le type d'aspect donné, ou None si non défini."""
    aspect_styles = {
        'Opposition': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},
        'Trigone': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
        'Carré': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},
        'Sextile': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
    }
    return aspect_styles.get(type_aspect)
    
    
    
def calculate_aspect_positions(pos1, pos2, rotation_offset):
    """Calcule les positions corrigées pour les lignes d'aspect en fonction de l'angle et du décalage."""
    angle1 = np.radians(pos1) + rotation_offset
    angle2 = np.radians(pos2) + rotation_offset
    x1, y1 = 0.8 * np.cos(angle1), 0.8 * np.sin(angle1)
    x2, y2 = 0.8 * np.cos(angle2), 0.8 * np.sin(angle2)
    return x1, y1, x2, y2



def draw_aspects(ax, aspects, rotation_offset):
    # Paramètres de style pour chaque type d'aspect
    aspect_styles = {
        'Opposition': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},  # Tirets longs
        'Trigone': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
        'Carré': {'color': 'red', 'linestyle': (0, (10, 5)), 'linewidth': 1.0},  # Tirets longs
        'Sextile': {'color': 'blue', 'linestyle': '-', 'linewidth': 0.8},
    }

    for aspect in aspects:
        type_aspect, pos1, pos2 = aspect
        # Appel de la fonciotn pour Obtenir le style pour le type d'aspect : def get_aspect_style
        style = get_aspect_style(type_aspect)
        if not style:
            continue


        # Appel de la fonciotn pour Appliquer le décalage de rotation et... :  def calculate_aspect_positions
        # Calculer les positions des extrémités des lignes d'aspect
        x1, y1, x2, y2 = calculate_aspect_positions(pos1, pos2, rotation_offset)


        # Dessiner la ligne d'aspect
        ax.plot([x1, x2], [y1, y2], color=style['color'], linestyle=style['linestyle'], linewidth=style['linewidth'], zorder=10)


