import ast
import os

def extract_classes_and_variables_from_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    classes = {"global_variables": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            classes[class_name] = {"attributes": [], "methods": []}
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    classes[class_name]["methods"].append(child.name)
                elif isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            classes[class_name]["attributes"].append(target.id)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    classes["global_variables"].append(target.id)
    return classes

def extract_functions_from_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return functions

def scan_project_directory(directory):
    all_details = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                classes = extract_classes_and_variables_from_file(file_path)
                functions = extract_functions_from_file(file_path)
                all_details[file_path] = {"classes": classes, "functions": functions}
    return all_details

if __name__ == "__main__":
    project_directory = "/mnt/e/CALENDAR/astro"  # Remplace par le chemin de ton projet
    details_dict = scan_project_directory(project_directory)
    for file, details in details_dict.items():
        print(f"\nFile: {file}")
        if details["classes"]:
            for class_name, class_details in details["classes"].items():
                if class_name == "global_variables":
                    print(f"  Global Variables: {class_details}")
                else:
                    print(f"  Class: {class_name}")
                    print(f"    Attributes: {class_details['attributes']}")
                    print(f"    Methods: {class_details['methods']}")
        if details["functions"]:
            print(f"  Functions: {details['functions']}")
