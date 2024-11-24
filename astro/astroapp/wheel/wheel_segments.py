from matplotlib import patches
import numpy as np

def get_segment_colors():
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]
    return colors_outer, colors_inner
    
    
    
def draw_single_segment(ax, color_outer, color_inner, theta1, theta2):
    """Dessine un segment astrologique en deux arcs (extérieur et intérieur) avec des couleurs spécifiques."""
    # Dessiner l'arc extérieur
    arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
    ax.add_patch(arc_outer)

    # Dessiner l'arc intérieur
    arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
    ax.add_patch(arc_inner)



def draw_segments(ax, rotation_offset):
    # Appel de la fonciton pour les Couleurs des segments par élément (feu, terre, air, eau) : def get_segment_colors
    colors_outer, colors_inner = get_segment_colors()

    # Dessiner chaque segment pour les 12 signes
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        # Calculer l'angle de début pour chaque segment
        angle = 2 * np.pi / 12 * i
        angle_corrected = angle + rotation_offset

        # Définir les angles de chaque arc en degrés
        theta1 = np.degrees(angle_corrected)
        theta2 = np.degrees(angle_corrected + 2 * np.pi / 12)

        # Appel de la fonction pour Dessiner les arcs extérieur et intérieur pour chaque segment : def draw_single_segment
        draw_single_segment(ax, color_outer, color_inner, theta1, theta2)
        
        
        
def draw_main_divisions(ax, rotation_offset):
    """Dessine les divisions principales de 30° pour chaque signe."""
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        angle_corrected = angle + rotation_offset
        x_outer = 1.2 * np.cos(angle_corrected)
        y_outer = 1.2 * np.sin(angle_corrected)
        x_inner = 0.8 * np.cos(angle_corrected)
        y_inner = 0.8 * np.sin(angle_corrected)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)
        
        
        
def draw_subdivisions(ax, rotation_offset):
    """Dessine les subdivisions de 5° entre chaque division principale."""
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            sub_angle_corrected = sub_angle + rotation_offset
            x_sub = 1.2 * np.cos(sub_angle_corrected)
            y_sub = 1.2 * np.sin(sub_angle_corrected)
            x_sub_inner = 1.1 * np.cos(sub_angle_corrected)
            y_sub_inner = 1.1 * np.sin(sub_angle_corrected)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)
            
            
            
def draw_divisions(ax, rotation_offset):
    # Appel de la fonction pour ajouter les divisions principales de 30° pour chaque signe : def draw_main_divisions
    draw_main_divisions(ax, rotation_offset)

    # Appel de la fonction pour ajouter les subdivisions de 5° entre chaque division principale : def draw_subdivisions
    draw_subdivisions(ax, rotation_offset)