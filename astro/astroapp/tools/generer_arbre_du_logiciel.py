import os

def generer_arbre(repertoire, niveau=0):
    """Parcourt le répertoire et affiche son contenu sous forme d'arborescence."""
    try:
        for element in os.listdir(repertoire):
            chemin = os.path.join(repertoire, element)
            # Indenter selon le niveau
            indentation = "    " * niveau
            # Afficher les dossiers et fichiers
            if os.path.isdir(chemin):
                print(f"{indentation}📂 {element}/")
                generer_arbre(chemin, niveau + 1)
            else:
                print(f"{indentation}📄 {element}")
    except PermissionError:
        print(f"Permission refusée pour accéder à : {repertoire}")

def sauvegarder_arbre(repertoire, fichier_sortie):
    """Enregistre l'arborescence dans un fichier."""
    with open(fichier_sortie, 'w', encoding='utf-8') as fichier:
        original_stdout = os.sys.stdout
        os.sys.stdout = fichier
        try:
            generer_arbre(repertoire)
        finally:
            os.sys.stdout = original_stdout

if __name__ == "__main__":
    # Chemin du répertoire racine (remplace par ton chemin de projet)
    chemin_projet = input("Entrez le chemin du projet : ").strip()
    
    # Nom du fichier pour sauvegarder l'arbre
    fichier_sortie = "arbre_du_logiciel.txt"
    
    # Générer et afficher l'arbre dans la console
    print("\nArborescence du logiciel :\n")
    generer_arbre(chemin_projet)
    
    # Sauvegarder l'arbre dans un fichier
    sauvegarder_arbre(chemin_projet, fichier_sortie)
    print(f"\nArborescence enregistrée dans le fichier : {fichier_sortie}")
