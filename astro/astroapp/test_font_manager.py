from matplotlib import font_manager
import os

# Test pour vérifier l'utilisation de font_manager
font_path = os.path.join(os.getcwd(), 'astroapp/fonts/hamburgsymbols/HamburgSymbols.ttf')
prop = font_manager.FontProperties(fname=font_path)

print("La police est correctement chargée : ", prop)
