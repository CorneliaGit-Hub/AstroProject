
# 2-Fonction pour convertir les degrés en degrés, minutes et secondes
def convert_to_dms(degree):
    degrees = int(degree)
    minutes = int((degree - degrees) * 60)
    seconds = round(((degree - degrees) * 60 - minutes) * 60, 2)
    return degrees, minutes, seconds
