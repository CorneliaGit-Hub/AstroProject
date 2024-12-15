import swisseph as swe
import logging

# Initialisation du logger
logger = logging.getLogger(__name__)

# Liste des signes chinois
CHINESE_ZODIAC_SIGNS = [
    "Rat", "Buffle", "Tigre", "Lapin", "Dragon", "Serpent",
    "Cheval", "Chèvre", "Singe", "Coq", "Chien", "Cochon"
]

def get_chinese_zodiac(julian_day):
    """
    Calcule le signe chinois en fonction du jour julien, en prenant en compte
    le changement d'année au zéro degré Verseau.

    Args:
        julian_day (float): Jour julien.

    Returns:
        str: Le signe chinois correspondant.
    """
    try:
        # Étape 1 : Extraire l'année et convertir le jour julien
        year, month, day, _ = swe.revjul(julian_day)
        logger.debug(f"Année extraite du jour julien : {year}, mois : {month}, jour : {day}")

        # Étape 2 : Calculer le jour julien du début de l'année
        jd_start_of_year = swe.julday(year, 1, 1)
        logger.debug(f"Jour julien du début de l'année {year} : {jd_start_of_year}")

        # Étape 3 : Calcul du Nouvel An chinois (zéro degré Verseau)
        try:
            result = swe.solcross_ut(jd_start_of_year, 300.0)  # 300° = 0° Verseau
            if isinstance(result, float):  # Si un float est retourné
                chinese_new_year_jd = result
                logger.debug(f"Jour julien du Nouvel An chinois (retour float) : {chinese_new_year_jd}")
            elif isinstance(result, (list, tuple)) and len(result) == 2:  # Si un tuple est retourné
                flag, transit_info = result
                chinese_new_year_jd = transit_info[0]
                logger.debug(f"Jour julien du Nouvel An chinois (retour tuple) : {chinese_new_year_jd}")
            else:
                raise ValueError(f"Résultat inattendu de swe.solcross_ut : {result}")
        except Exception as e:
            logger.error(f"Erreur lors du calcul du Nouvel An chinois avec swe.solcross_ut : {e}")
            return "Erreur"

        # Étape 4 : Comparer avec le jour julien donné pour ajuster l'année
        if julian_day < chinese_new_year_jd:  # Si avant le Nouvel An chinois
            year -= 1
            logger.debug(f"Jour julien avant le Nouvel An chinois, année ajustée : {year}")

        # Étape 5 : Calculer le signe chinois
        index = (year - 4) % 12  # 4 correspond à l'année du Rat en 1924
        chinese_sign = CHINESE_ZODIAC_SIGNS[index]
        logger.debug(f"Signe chinois déterminé : {chinese_sign}")
        return chinese_sign

    except Exception as e:
        logger.error(f"Erreur lors du calcul du signe chinois : {e}")
        return "Erreur"



