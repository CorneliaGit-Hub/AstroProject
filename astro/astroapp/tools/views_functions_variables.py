import ast

class OrderedFunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.ordered_functions = []

    def visit_FunctionDef(self, node):
        # Stocker le nom de la fonction, ses arguments, et sa docstring
        function_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "variables": [],
            "docstring": ast.get_docstring(node),
            "lineno": node.lineno  # Enregistre le numéro de ligne pour garder l'ordre
        }

        # Ajouter les variables locales définies dans la fonction
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Assign):
                for target in sub_node.targets:
                    if isinstance(target, ast.Name):
                        function_info["variables"].append(target.id)

        self.ordered_functions.append(function_info)
        self.generic_visit(node)

# Charger le fichier views.py pour l'analyser
with open('views.py', 'r', encoding='utf-8') as file:
    tree = ast.parse(file.read())

analyzer = OrderedFunctionAnalyzer()
analyzer.visit(tree)

# Trier les fonctions par numéro de ligne pour les afficher dans l'ordre d'apparition
analyzer.ordered_functions.sort(key=lambda x: x["lineno"])

# Affichage de toutes les fonctions avec numérotation dans l'ordre d'apparition
print(f"Nombre total de fonctions trouvées : {len(analyzer.ordered_functions)}\n")
for index, func in enumerate(analyzer.ordered_functions, start=1):
    print(f"Fonction {index}: {func['name']}")
    print(f"  Arguments : {', '.join(func['args'])}")
    print(f"  Variables locales : {', '.join(func['variables'])}")
    if func['docstring']:
        print(f"  Description : {func['docstring']}")
    else:
        print("  Description : Aucune description")
    print()

# Vérification des fonctions sans description
missing_descriptions = [func for func in analyzer.ordered_functions if not func['docstring']]
if missing_descriptions:
    print("Fonctions manquant de descriptions :")
    for func in missing_descriptions:
        print(f"- {func['name']}")
else:
    print("Toutes les fonctions ont une description.")
