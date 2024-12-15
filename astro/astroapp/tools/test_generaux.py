import swisseph as swe
import os

from astroapp.utils.chinese_zodiac import get_chinese_zodiac

# Définir le chemin des éphémérides
ephemeris_path = "/mnt/e/CALENDAR/ephemerides/ephe"  # Chemin pour WSL
swe.set_ephe_path(ephemeris_path)




# Initialisation de quelques jours juliens pour les tests
test_cases = [
    (2448976.5, "Avant le Nouvel An chinois 1993 (1er janvier)"),
    (2449399.5, "Après le Nouvel An chinois 1994 (10 février)"),
    (2449600.5, "Date intermédiaire en 1994"),
    (2450449.5, "Avant le Nouvel An chinois 1996 (31 janvier)"),
]

for jd, description in test_cases:
    try:
        result = get_chinese_zodiac(jd)
        print(f"Jour Julien : {jd} | Description : {description} | Signe Chinois : {result}")
    except Exception as e:
        print(f"Erreur lors du calcul pour le jour julien {jd} : {e}")
