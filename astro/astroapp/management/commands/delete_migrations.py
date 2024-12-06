from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Supprime les entrées de migration de l'application astroapp dans la base de données."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'astroapp';")
            self.stdout.write(self.style.SUCCESS("Les migrations pour 'astroapp' ont été supprimées de la base de données."))
