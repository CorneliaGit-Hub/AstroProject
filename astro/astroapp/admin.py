from django.contrib import admin
from .models import ThemeAstrologique

@admin.register(ThemeAstrologique)
class ThemeAstrologiqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthdate', 'birthtime', 'country_of_birth', 'city_of_birth', 'utilisateur', 'date_de_creation')
    search_fields = ('name', 'utilisateur__username', 'city_of_birth', 'country_of_birth')

