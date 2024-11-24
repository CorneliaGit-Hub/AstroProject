import os
import matplotlib.pyplot as plt

def remove_existing_image(image_path):
    """Supprime l'image existante à un chemin donné si elle est présente."""
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Ancienne image supprimée : {image_path}")
    else:
        print(f"Aucune ancienne image à supprimer : {image_path}")


def save_astrological_image(fig, image_path):

    # Appel de la fonction pour supprimer l'image existante si elle existe : def remove_existing_image
    remove_existing_image(image_path)


    # Sauvegarder la nouvelle image générée
    try:
        fig.savefig(image_path, dpi=300)
        print(f"L'image a été sauvegardée avec succès à : {image_path}")
    except Exception as e:
        print(f"Erreur lors de la génération de l'image : {e}")
    finally:
        plt.close(fig)  # Fermer la figure pour libérer la mémoire

