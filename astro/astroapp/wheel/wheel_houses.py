import numpy as np
from matplotlib import patches


# Les lignes
def add_house_cusps(ax, house_results, rotation_offset):
    """Ajoute les lignes de cuspides pour chaque maison sur la roue astrologique."""
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle en degrés pour chaque cuspide de maison
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Calculer la position pour la ligne de la cuspide de la maison
        x_pos = 1.27 * np.cos(angle_corrected)
        y_pos = 1.27 * np.sin(angle_corrected)
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)  # Ligne de cuspide de maison



# Les Triangles
def add_house_triangles(ax, house_results, rotation_offset):
    """Ajoute les triangles pour marquer les cuspides des maisons principales et secondaires."""
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle_corrected = np.radians(degree) + rotation_offset
        x_triangle = 1.26 * np.cos(angle_corrected)
        y_triangle = 1.26 * np.sin(angle_corrected)
        facecolor = 'black' if i + 1 in [1, 4, 7, 10] else 'white'
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05,
                                          orientation=angle_corrected + np.pi / 2,
                                          edgecolor='black', facecolor=facecolor,
                                          linewidth=1.0, zorder=3)
        ax.add_patch(triangle)
        
        
        
# Les lignes et les triangles
def draw_houses_and_cusps(ax, house_results, rotation_offset):
    # Appel de la fonction pour ajouter les LIGNES de cuspides pour chaque maison : def add_house_cusps
    add_house_cusps(ax, house_results, rotation_offset)

    # Appel de la fonction pour ajouter les TRIANGLES pour chaque maison : def add_house_triangles
    add_house_triangles(ax, house_results, rotation_offset)
    
    
    
def display_house_degrees(ax, house_results, rotation_offset):
    """Affiche les degrés et minutes pour chaque cuspide de maison sur la roue astrologique."""
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        degree_in_sign = degree % 30
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)

        x_degree = 1.38 * np.cos(angle_corrected)
        y_degree = 1.38 * np.sin(angle_corrected)
        
        x_minutes = 1.5 * np.cos(angle_corrected)
        y_minutes = 1.5 * np.sin(angle_corrected)
        
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=11, 
                ha='center', va='center', color='black')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, 
                ha='center', va='center', color='black')
                
                
                
def get_roman_numerals():
    """Renvoie un dictionnaire associant les numéros de maisons aux chiffres romains."""
    return {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }
    
    
    
def calculate_house_position(degree_start, degree_end, rotation_offset):
    """Calcule la position x, y pour un numéro de maison au centre de son segment."""
    if degree_end < degree_start:
        degree_end += 360
    degree_mid = (degree_start + degree_end) / 2
    angle_mid = np.radians(degree_mid) + rotation_offset
    x_text = 1.28 * np.cos(angle_mid)
    y_text = 1.28 * np.sin(angle_mid)
    return x_text, y_text
    
    
    
def draw_house_numbers(ax, house_results, rotation_offset):
    # Dictionnaire pour convertir les numéros de maisons en chiffres romains


    # Positionner chaque numéro de maison au centre de son segment
    for i in range(len(house_results)):
        # Obtenir les angles des cuspides de chaque maison
        degree_start = house_results[f'Maison {i + 1}']['degree']
        degree_end = house_results[f'Maison {(i + 2) if (i + 2) <= 12 else 1}']['degree']
        
        # Appel de la fonciton pour Ajuster si le segment traverse 0° : def calculate_house_position
        x_text, y_text = calculate_house_position(degree_start, degree_end, rotation_offset)
        
        # Appel de la fonciton pour Afficher le numéro de maison au centre de chaque segment : def get_roman_numerals
        roman_house_num = get_roman_numerals()[i + 1]
        
        ax.text(x_text, y_text, roman_house_num, fontsize=12, ha='center', va='center', color='black', weight='bold')
        
        
        
