import os

def list_imports_in_file(file_path):
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return imports

def list_all_imports_in_directory(directory_path):
    all_imports = set()
    print(f"Parcourir le répertoire : {directory_path}")
    try:
        for subdir, dirs, files in os.walk(directory_path):
            print(f"Visite du sous-répertoire : {subdir}")
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(subdir, file)
                    print(f"Traitement du fichier : {file_path}")
                    imports = list_imports_in_file(file_path)
                    all_imports.update(imports)
    except Exception as e:
        print(f"Erreur lors du parcours des répertoires : {e}")
    return all_imports

# Specify the path to the directory containing Python files
project_directory = '/mnt/e/CALENDAR/astro/astroapp'
all_imports = list_all_imports_in_directory(project_directory)
if all_imports:
    for imp in sorted(all_imports):
        print(imp)
else:
    print("Aucun import trouvé.")
