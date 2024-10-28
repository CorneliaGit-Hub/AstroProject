# ROUE
def generate_astrological_wheel(planet_positions, house_results):
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

    # Ajuster les limites de l'axe pour ne pas couper les angles
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-2.9, 2.9)

    # Supprimer les marges automatiques et régler la figure pour occuper tout l'espace
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.set_size_inches(12, 12)
    ax.set_aspect('equal')
    
    # Sauvegarder l'image finale
    save_astrological_image(fig, image_path)




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

def draw_segments(ax, rotation_offset):
    # Couleurs des segments par élément (feu, terre, air, eau)
    colors_outer = ["#ffbfbf", "#ffdcc0", "#ffeac1", "#fff3bf", "#ffffbf", "#e7fbbe", 
                    "#c0f2bf", "#bfe6e5", "#c4cfeb", "#ccc4eb", "#ccc4eb", "#f1bfda"]
    colors_inner = ["#ffcccb", "#ffe3cb", "#ffe3cd", "#fff6cd", "#ffffcd", "#edfcd5", 
                    "#ccf5cd", "#cceaec", "#d0d8ed", "#d7d0ef", "#d7d0ef", "#f6cce4"]

    # Dessiner chaque segment pour les 12 signes
    for i, (color_outer, color_inner) in enumerate(zip(colors_outer, colors_inner)):
        # Calculer l'angle de début pour chaque segment
        angle = 2 * np.pi / 12 * i
        angle_corrected = angle + rotation_offset

        # Définir les angles de chaque arc en degrés
        theta1 = np.degrees(angle_corrected)
        theta2 = np.degrees(angle_corrected + 2 * np.pi / 12)

        # Dessiner l'arc extérieur pour chaque segment
        arc_outer = patches.Wedge(center=(0, 0), r=1.2, theta1=theta1, theta2=theta2, facecolor=color_outer, zorder=2)
        ax.add_patch(arc_outer)

        # Dessiner l'arc intérieur pour chaque segment
        arc_inner = patches.Wedge(center=(0, 0), r=1.09, theta1=theta1, theta2=theta2, facecolor=color_inner, zorder=2)
        ax.add_patch(arc_inner)


def draw_divisions(ax, rotation_offset):
    # Ajouter les divisions principales de 30° pour chaque signe
    for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        # Calculer la position corrigée de l'angle pour chaque division majeure
        angle_corrected = angle + rotation_offset
        x_outer = 1.2 * np.cos(angle_corrected)
        y_outer = 1.2 * np.sin(angle_corrected)
        x_inner = 0.8 * np.cos(angle_corrected)
        y_inner = 0.8 * np.sin(angle_corrected)
        ax.plot([x_outer, x_inner], [y_outer, y_inner], 'k', lw=1)  # Division principale de 30°

        # Ajouter les subdivisions de 5° entre chaque division principale
        for sub_angle in np.linspace(angle, angle + np.pi / 6, 6, endpoint=False):
            sub_angle_corrected = sub_angle + rotation_offset
            x_sub = 1.2 * np.cos(sub_angle_corrected)
            y_sub = 1.2 * np.sin(sub_angle_corrected)
            x_sub_inner = 1.1 * np.cos(sub_angle_corrected)
            y_sub_inner = 1.1 * np.sin(sub_angle_corrected)
            ax.plot([x_sub, x_sub_inner], [y_sub, y_sub_inner], 'k', lw=0.5)  # Subdivision de 5°


def draw_zodiac_symbols(ax, rotation_offset):
    # Les éléments associés aux signes du zodiaque
    elements = ['fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water', 
                'fire', 'earth', 'air', 'water']

    # Couleurs par élément
    sign_colors = {
        'fire': "#f9074c",   # Bélier, Lion, Sagittaire
        'earth': "#c59626",  # Taureau, Vierge, Capricorne
        'air': "#1a8fe9",    # Gémeaux, Balance, Verseau
        'water': "#62ce02"   # Cancer, Scorpion, Poissons
    }

    # Liste des symboles zodiacaux (en utilisant des symboles unicode ou police spécifique)
    zodiac_symbols = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'v', 'x', 'c']
    
    # Charger la police HamburgSymbols si nécessaire
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

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


def draw_planet_positions(ax, planet_positions, rotation_offset):
    # Symboles pour chaque planète (utilisation d'une police ou de symboles Unicode)
    planet_symbols = {
        'Soleil': 'Q', 'Lune': 'W', 'Mercure': 'E', 'Vénus': 'R', 
        'Mars': 'T', 'Jupiter': 'Y', 'Saturne': 'U', 'Uranus': 'I', 
        'Neptune': 'O', 'Pluton': 'P'
    }
    
    # Couleurs pour chaque planète
    planet_colors = {
        'Soleil': '#FFA801', 'Lune': '#FFA801', 'Mercure': '#A9CE02', 'Vénus': '#BB55A1',
        'Mars': '#F9074C', 'Jupiter': '#07B3F2', 'Saturne': '#6A3D90', 
        'Uranus': '#9B207B', 'Neptune': '#07B3F2', 'Pluton': '#3B2B7B'
    }
    
    # Police HamburgSymbols pour les symboles planétaires
    font_path = os.path.join(settings.BASE_DIR, 'astroapp', 'fonts', 'hamburgsymbols', 'HamburgSymbols.ttf')
    prop = font_manager.FontProperties(fname=font_path)

    # Placer chaque planète à sa position respective
    for planet, degree in planet_positions:
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
def draw_houses_and_cusps(ax, house_results, rotation_offset):
    # Ajouter les lignes de cuspides pour chaque maison
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle en degrés pour chaque cuspide de maison
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Calculer la position pour la ligne de la cuspide de la maison
        x_pos = 1.27 * np.cos(angle_corrected)
        y_pos = 1.27 * np.sin(angle_corrected)
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.7, zorder=1)  # Ligne de cuspide de maison

    # Ajouter des triangles pour marquer toutes les maisons, avec des couleurs spécifiques pour les maisons principales
    for i, (house, house_data) in enumerate(house_results.items()):
        # Récupérer l'angle pour le triangle de la maison
        degree = house_data['degree']
        angle_corrected = np.radians(degree) + rotation_offset
        
        # Calculer la position du triangle sur la roue
        x_triangle = 1.26 * np.cos(angle_corrected)
        y_triangle = 1.26 * np.sin(angle_corrected)
        
        # Définir la couleur du triangle : noir pour les maisons principales, blanc pour les autres
        facecolor = 'black' if i + 1 in [1, 4, 7, 10] else 'white'
        
        # Ajouter le triangle avec la couleur appropriée
        triangle = patches.RegularPolygon((x_triangle, y_triangle), numVertices=3, radius=0.05,
                                          orientation=angle_corrected + np.pi / 2,  # Orientation pour qu'il pointe vers le cercle
                                          edgecolor='black', facecolor=facecolor,
                                          linewidth=1.0, zorder=3)
        ax.add_patch(triangle)



def display_degrees(ax, planet_positions, house_results, rotation_offset):
    # Affichage des degrés pour chaque planète
    for planet, degree in planet_positions:
        # Calculer la position corrigée de l'angle pour les degrés de chaque planète
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        # Conversion des degrés en position dans le signe
        sign_number = int(degree // 30)  # Déterminer le signe
        degree_in_sign = degree % 30  # Degré dans le signe
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)  # Minutes dans le signe

        # Position pour les degrés de la planète
        x_degree = 1.94 * np.cos(angle_corrected)
        y_degree = 1.94 * np.sin(angle_corrected)
        
        # Position pour les minutes de la planète (plus éloigné)
        x_minutes = 2.10 * np.cos(angle_corrected)
        y_minutes = 2.10 * np.sin(angle_corrected)
        
        # Afficher les degrés et minutes de la planète
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=13, 
                ha='center', va='center', color='black', weight='bold')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=11, 
                ha='center', va='center', color='black', weight='bold')

    # Affichage des degrés pour chaque cuspide de maison
    for i, (house, house_data) in enumerate(house_results.items()):
        degree = house_data['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset
        
        # Conversion en degrés et minutes
        degree_in_sign = degree % 30  # Degré dans le signe
        minutes = int((degree_in_sign - int(degree_in_sign)) * 60)  # Minutes dans le signe

        # Position des degrés et minutes de la maison
        x_degree = 1.38 * np.cos(angle_corrected)  # Proche du cercle
        y_degree = 1.38 * np.sin(angle_corrected)
        
        x_minutes = 1.5 * np.cos(angle_corrected)  # Légèrement plus éloigné
        y_minutes = 1.5 * np.sin(angle_corrected)
        
        # Afficher les degrés et minutes de la maison
        ax.text(x_degree, y_degree, f"{int(degree_in_sign)}°", fontsize=11, 
                ha='center', va='center', color='black')
        ax.text(x_minutes, y_minutes, f"{minutes}'", fontsize=8, 
                ha='center', va='center', color='black')



def draw_asc_mc_lines(ax, house_results, rotation_offset):
    # Dictionnaire pour associer ASC et MC aux maisons
    asc_mc_houses = {'ASC': 'Maison 1', 'MC': 'Maison 10'}

    # Ajouter une ligne et un marqueur pour chaque élément (ASC et MC)
    for label, house_key in asc_mc_houses.items():
        degree = house_results[house_key]['degree']
        angle = np.radians(degree)
        angle_corrected = angle + rotation_offset

        # Calcul des coordonnées de fin pour la ligne
        x_pos = 2.3 * np.cos(angle_corrected)
        y_pos = 2.3 * np.sin(angle_corrected)

        # Tracer la ligne du centre à la position de l'ASC ou MC
        ax.plot([0, x_pos], [0, y_pos], color='black', lw=0.5, zorder=1)

        # Ajouter un triangle (flèche) pour l'ASC et un cercle pour le MC
        if label == 'ASC':
            triangle = patches.RegularPolygon((x_pos, y_pos), numVertices=3, radius=0.20,
                                              orientation=angle + rotation_offset + np.radians(270),
                                              edgecolor='black', facecolor='white', lw=0.5, zorder=3)
            ax.add_patch(triangle)

            # Placer le label "ASC"
            ax.text(x_pos + 0.4 * np.cos(angle_corrected), y_pos + 0.4 * np.sin(angle_corrected), 
                    'ASC', fontsize=12, ha='center', va='center', color='black', weight='bold')

        elif label == 'MC':
            circle = plt.Circle((x_pos, y_pos), 0.20, facecolor='white', edgecolor='black', lw=0.5, zorder=2)
            ax.add_patch(circle)

            # Placer le label "MC"
            ax.text(x_pos + 0.35 * np.cos(angle_corrected), y_pos + 0.35 * np.sin(angle_corrected), 
                    'MC', fontsize=12, ha='center', va='center', color='black', weight='bold')



def draw_house_numbers(ax, house_results, rotation_offset):
    # Dictionnaire pour convertir les numéros de maisons en chiffres romains
    roman_numerals = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII",
        9: "IX", 10: "X", 11: "XI", 12: "XII"
    }

    # Positionner chaque numéro de maison au centre de son segment
    for i in range(len(house_results)):
        # Obtenir les angles des cuspides de chaque maison
        degree_start = house_results[f'Maison {i + 1}']['degree']
        degree_end = house_results[f'Maison {(i + 2) if (i + 2) <= 12 else 1}']['degree']
        
        # Ajuster si le segment traverse 0°
        if degree_end < degree_start:
            degree_end += 360

        # Calculer l'angle médian de la maison
        degree_mid = (degree_start + degree_end) / 2
        angle_mid = np.radians(degree_mid)
        angle_mid_corrected = angle_mid + rotation_offset

        # Positionner le numéro de la maison
        x_text = 1.3 * np.cos(angle_mid_corrected)
        y_text = 1.3 * np.sin(angle_mid_corrected)
        
        # Afficher le numéro de maison au centre de chaque segment
        roman_house_num = roman_numerals[i + 1]
        ax.text(x_text, y_text, roman_house_num, fontsize=12, ha='center', va='center', color='black', weight='bold')






# FIN 
def save_astrological_image(fig, image_path):
    # Supprimer l'ancienne image si elle existe
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Ancienne image supprimée : {image_path}")
    else:
        print(f"Aucune ancienne image à supprimer : {image_path}")

    # Sauvegarder la nouvelle image générée
    try:
        fig.savefig(image_path, dpi=300)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")
    finally:
        plt.close(fig)  # Fermer la figure pour libérer la mémoire
