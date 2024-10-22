"""
WSGI config for astroconfig project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named 'application'. Django's 'runserver' and 'gunicorn' are two examples of
servers that use this configuration pattern.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module accordingly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroconfig.settings')

application = get_wsgi_application()
