import os
import numpy as np
from matplotlib import pyplot as plt
from astroapp.utils.files_utils import save_astrological_image
from astroapp.wheel.wheel_symbols import draw_zodiac_symbols, display_planet_degrees, get_planet_colors
from astroapp.wheel.wheel_houses import draw_houses_and_cusps, draw_house_numbers, display_house_degrees
from astroapp.wheel.wheel_segments import draw_segments, draw_divisions
from astroapp.wheel.wheel_aspects import draw_aspects
from django.conf import settings
from astroapp.utils.planet_utils import draw_planet_positions
from astroapp.wheel.wheel_houses import draw_asc_mc_lines
from astroapp.wheel.wheel_houses import draw_asc_mc_marker





def create_astrological_figure():
    # Créer la figure et les axes avec la taille et les limites appropriées
    fig, ax = plt.subplots(figsize=(14, 14))  # Dimensions de la figure (modifiables si nécessaire)
    ax.set_xlim(-1.5, 1.5)  # Limites de l'axe x
    ax.set_ylim(-1.5, 1.5)  # Limites de l'axe y
    ax.set_aspect('equal')  # Proportions égales pour un cercle parfait
    ax.axis('off')  # Masquer les axes pour un rendu propre de la roue astrologique
    
    return fig, ax
    
    
    
def draw_circle(ax):
    # Dessiner le cercle principal qui forme la base de la roue astrologique
    main_circle = plt.Circle((0, 0), 1.2, edgecolor='black', facecolor='none', linewidth=1)
    ax.add_patch(main_circle)
    
    # Ajouter un cercle blanc au centre pour dégager la zone centrale
    center_circle = plt.Circle((0, 0), 0.80, color='white', ec='black', linewidth=0.5, zorder=10)
    ax.add_patch(center_circle)
    
    # Ajouter un cercle extérieur pour la bordure de la roue
    outer_border_circle = plt.Circle((0, 0), 1.2, color='none', ec='black', linewidth=0.5, zorder=5)
    ax.add_patch(outer_border_circle)
    
    
    
def display_degrees(ax, planet_positions, house_results, rotation_offset):
    # Appelle de la fonction du Dictionnaire des couleurs des planètes : def get_planet_colors
    planet_colors = get_planet_colors()

    # Appelle de la fonction pour l'Affichage des degrés pour chaque planète : def display_planet_degrees
    display_planet_degrees(ax, planet_positions, rotation_offset, planet_colors)

    # Appelle de la fonction pour l'Affichage des degrés pour chaque cuspide de maison (en noir) : def display_house_degrees
    display_house_degrees(ax, house_results, rotation_offset)



# Fonction générale pour appeler les sous foncitons.
def generate_astrological_wheel(planet_positions, house_results, aspects):
    # Définir le chemin d'image
    image_path = os.path.join(settings.BASE_DIR, 'astroapp/static/images/zodiac_wheel.png')

    # Initialiser la figure et les axes
    fig, ax = create_astrological_figure()

    # Calculer l’offset de rotation pour aligner l'ascendant à gauche
    asc_angle = house_results['Maison 1']['degree']
    rotation_offset = np.radians(-asc_angle + 180)

    # Dessiner le cercle principal
    draw_circle(ax)

    # Dessiner les segments colorés des signes
    draw_segments(ax, rotation_offset)

    # Ajouter les divisions principales et les subdivisions
    draw_divisions(ax, rotation_offset)

    # Placer les symboles des signes du zodiaque
    draw_zodiac_symbols(ax, rotation_offset)

    # Positionner les symboles des planètes selon leurs positions calculées et ajouter les lignes de liaison
    draw_planet_positions(ax, planet_positions, rotation_offset)

    # Ajouter les cuspides des maisons et les triangles pour les maisons principales
    draw_houses_and_cusps(ax, house_results, rotation_offset)

    # Afficher les degrés et minutes pour chaque planète et chaque maison
    display_degrees(ax, planet_positions, house_results, rotation_offset)

    # Ajouter les lignes pour l'ASC et le MC avec leurs marqueurs
    draw_asc_mc_lines(ax, house_results, rotation_offset)

    # Ajouter les numéros des maisons
    draw_house_numbers(ax, house_results, rotation_offset)
    
    # Appeler draw_aspects pour dessiner les aspects
    draw_aspects(ax, aspects, rotation_offset)


    # Ajuster les limites de l'axe pour ne pas couper les angles
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-2.9, 2.9)

    # Supprimer les marges automatiques et régler la figure pour occuper tout l'espace
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.set_size_inches(12, 12)
    ax.set_aspect('equal')
    
    # Sauvegarder l'image finale
    save_astrological_image(fig, image_path)
