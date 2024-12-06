import os
import matplotlib.pyplot as plt

def remove_existing_image(image_path):
    """
    Supprime l'image existante à un chemin donné si elle est présente.

    Args:
        image_path (str): Le chemin absolu de l'image à supprimer.

    Returns:
        bool: True si l'image a été supprimée avec succès, False sinon.
    """
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"DEBUG - Ancienne image supprimée avec succès : {image_path}")
            return True
        except Exception as e:
            print(f"DEBUG - Erreur lors de la suppression de l'image {image_path} : {e}")
            return False
    else:
        print(f"DEBUG - Image introuvable ou déjà supprimée : {image_path}")
        return False



def save_astrological_image(fig, image_path, session):
    # Débogage : Vérification de l'image précédente dans la session
    if 'last_generated_image' in session:
        previous_image = session['last_generated_image']
        print(f"DEBUG - Image précédente à supprimer : {previous_image}")
        remove_existing_image(previous_image)
    else:
        print("DEBUG - Aucune image précédente enregistrée dans la session.")

    # Sauvegarder la nouvelle image générée
    try:
        fig.savefig(image_path, dpi=300)
        print(f"DEBUG - Image sauvegardée avec succès : {image_path}")
    except Exception as e:
        print(f"DEBUG - Erreur lors de la sauvegarde de l'image : {e}")
    finally:
        plt.close(fig)  # Libérer la mémoire
        print("DEBUG - Figure matplotlib fermée.")

    # Mettre à jour la session avec la nouvelle image
    session['last_generated_image'] = image_path
    print(f"DEBUG - Nouvelle image enregistrée dans la session : {session['last_generated_image']}")



