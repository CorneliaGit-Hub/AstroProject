import matplotlib.pyplot as plt

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
    
    
    


