from django import template

register = template.Library()

@register.filter
def degrees_minutes(value):
    degrees = int(value)
    minutes = int((value - degrees) * 60)  # On tronque les minutes
    seconds = round(((value - degrees) * 60 - minutes) * 60, 2)
    return f"{degrees}°{minutes}'"
