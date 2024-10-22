import matplotlib.pyplot as plt
import os

def create_circle_image():
    image_path = '/mnt/e/CALENDAR/astro/astroapp/static/images/zodiac_wheel.png'
    fig, ax = plt.subplots()
    circle = plt.Circle((0.5, 0.5), 0.4, color='blue', fill=True)
    ax.add_artist(circle)
    ax.set_aspect('equal', adjustable='datalim')
    plt.axis('off')
    plt.savefig(image_path, format='png', dpi=300)
    plt.close()

if __name__ == "__main__":
    create_circle_image()
