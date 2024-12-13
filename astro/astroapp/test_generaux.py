import swisseph as swe

# Défini le chemin des éphémérides
swe.set_ephe_path("/mnt/e/CALENDAR/env/ephe")

# Tester un calcul simple
jd = swe.julday(2024, 1, 1, 0)  # Calcul du jour julien pour le 1er janvier 2024
planet_position, ret = swe.calc_ut(jd, swe.SUN)  # Calcul de la position du Soleil
print("Position du Soleil :", planet_position)
