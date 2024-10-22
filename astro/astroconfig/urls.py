from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('astroapp.urls')),  # Inclut les URLs de l'application `astroapp`
]
