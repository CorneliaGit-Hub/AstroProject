from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ThemeAstrologique, CustomUser

# Configuration pour le modèle CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)

# Configuration pour le modèle ThemeAstrologique
@admin.register(ThemeAstrologique)
class ThemeAstrologiqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthdate', 'birthtime', 'country_of_birth', 'city_of_birth', 'utilisateur', 'date_de_creation')
    search_fields = ('name', 'utilisateur__username', 'city_of_birth', 'country_of_birth')


