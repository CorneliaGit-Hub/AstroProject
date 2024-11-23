import os

def generate_code_report_by_files(base_path="/mnt/e/CALENDAR/astro"):
    """
    Affiche dans le terminal le contenu des fichiers Python dans un dossier donné et ses sous-dossiers,
    en excluant les dossiers '__pycache__' et les dossiers vides.
    """
    try:
        print(f"Rapport des fichiers Python dans : {base_path}\n")
        
        for root, dirs, files in os.walk(base_path):
            # Exclure les dossiers '__pycache__'
            dirs[:] = [d for d in dirs if d != "__pycache__"]

            # Vérifier si le dossier contient des fichiers Python
            python_files = [file for file in files if file.endswith(".py")]

            if python_files:  # On n'affiche que les dossiers contenant des fichiers Python
                print(f"Dossier : {root}")
                print("=" * (9 + len(root)))
                for file in python_files:
                    file_path = os.path.join(root, file)
                    print(f"\nFichier : {file}")
                    print("-" * (9 + len(file)))
                    try:
                        with open(file_path, "r", encoding="utf-8") as py_file:
                            print(py_file.read())
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier : {e}")
                    print("\n")
                print("\n")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")

if __name__ == "__main__":
    # Le chemin est défini par défaut pour `/mnt/e/CALENDAR/astro`
    generate_code_report_by_files()
