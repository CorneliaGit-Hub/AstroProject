

def calculate_angular_difference(pos1, pos2):
    """Calcule la différence angulaire minimale entre deux positions planétaires."""
    diff = abs(pos1 - pos2)
    return min(diff, 360 - diff)
    
    
    

def add_aspect_if_present(aspects, planet1, pos1, planet2, pos2, diff, aspect_definitions, aspect_orbs):
    """Vérifie si un aspect existe entre deux positions planétaires et l'ajoute à la liste des aspects."""
    for aspect_name, aspect_angle in aspect_definitions.items():
        orbe = aspect_orbs[aspect_name]
        if abs(diff - aspect_angle) <= orbe:
            aspects.append((aspect_name, pos1, pos2))



# Fonction pour afficher les aspects planétaires
def calculate_aspects(planet_positions):
    aspects = []
    aspect_definitions = {
        'Conjonction': 0,
        'Sextile': 60,
        'Carré': 90,
        'Trigone': 120,
        'Opposition': 180,
    }
    aspect_orbs = {
        'Conjonction': 8,
        'Sextile': 6,
        'Carré': 6,
        'Trigone': 8,
        'Opposition': 8,
    }

    for i in range(len(planet_positions)):
        for j in range(i + 1, len(planet_positions)):
            planet1, pos1 = planet_positions[i]
            planet2, pos2 = planet_positions[j]
            
            # Appel la fonction qui Calcule la différence angulaire minimale entre deux positions
            diff = calculate_angular_difference(pos1, pos2)


            # Appel la focntion qui Vérifie si un aspect est présent et l'ajoute s'il est détecté : def add_aspect_if_present
            add_aspect_if_present(aspects, planet1, pos1, planet2, pos2, diff, aspect_definitions, aspect_orbs)

    return aspects
    
    
    
# Fonction pour calculer les aspects planétaires
def calculate_astrological_aspects(planet_positions):
    aspects = calculate_aspects(planet_positions)
    return aspects
    
    



