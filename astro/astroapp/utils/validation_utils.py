

def validate_required_fields(fields, field_names):
    """
    Valide que tous les champs requis sont présents et non vides.

    Args:
        fields (list): Liste des champs à valider.
        field_names (list): Noms des champs correspondants pour afficher une erreur claire.

    Returns:
        tuple: (bool, str) - Booléen indiquant si tout est valide, et un message d'erreur le cas échéant.
    """
    missing_fields = [name for field, name in zip(fields, field_names) if not field]
    if missing_fields:
        return False, f"Les champs suivants sont manquants : {', '.join(missing_fields)}"
    return True, None
