import swisseph as swe

def calculate_julian_day(birth_datetime_utc):
    """
    Calcule le jour julien (JD) à partir d'une date UTC.
    :param birth_datetime_utc: datetime en UTC
    :return: float, jour julien
    """
    return swe.julday(
        birth_datetime_utc.year,
        birth_datetime_utc.month,
        birth_datetime_utc.day,
        birth_datetime_utc.hour
        + birth_datetime_utc.minute / 60
        + birth_datetime_utc.second / 3600,
    )

def calculate_julian_day_and_planet_positions(birth_datetime_utc, latitude, longitude):

    # Appel de la fonction pour calculer le jour julien (JD) : def calculate_julian_day
    jd = calculate_julian_day(birth_datetime_utc)

    
    # Calcul des positions des planètes
    results, planet_positions = calculate_planet_positions(jd)

    # Ajoute ce print ici
    print("Jour Julien Calculé :", jd)
    return jd, results, planet_positions