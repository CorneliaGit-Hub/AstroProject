def get_aspect_data():
    """
    Retourne les symboles et couleurs des aspects astrologiques,
    basés sur la police HamburgSymbols.
    """
    aspect_data = {
        'Conjonction': {'symbol': 'q', 'color': 'black'},
        'Semi-sextile': {'symbol': 'i', 'color': '#62ce02'},  # Vert
        'Semi-carré': {'symbol': 'y', 'color': 'orange'},
        'Sextile': {'symbol': 't', 'color': '#247eeb'},
        'Carré': {'symbol': 'r', 'color': 'red'},
        'Trigone': {'symbol': 'e', 'color': '#247eeb'},
        'Sesqui-carré': {'symbol': 'u', 'color': 'orange'},
        'Quinconce': {'symbol': 'o', 'color': '#c59626'},  # Marron
        'Opposition': {'symbol': 'w', 'color': 'red'},
    }
    return aspect_data
