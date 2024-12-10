from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your_secret_key_here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
LOGIN_URL = '/connexion/'
LOGIN_REDIRECT_URL = '/themes/'  # Redirige après connexion

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'astroapp',  # L'application 'astroapp'
]

AUTH_USER_MODEL = 'astroapp.CustomUser'  # Utilisation du modèle utilisateur personnalisé

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'astroconfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'astroconfig.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Dossier temporaire pour stocker les images astrologiques
TEMP_IMAGE_DIR = os.path.join(BASE_DIR, 'astroapp', 'static', 'images', 'temps')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sécurité des cookies et des sessions
SESSION_COOKIE_SECURE = False   # Empêche la transmission des cookies en HTTP non sécurisé

# Configuration des sessions Django
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Utilisation de la base de données pour les sessions
SESSION_COOKIE_AGE = 1209600  # Durée de la session en secondes (2 semaines)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Les sessions persistent même après la fermeture du navigateur

# Configuration des cookies CSRF
CSRF_COOKIE_SECURE = False  # Désactivé pour le développement local (HTTP)

SECURE_BROWSER_XSS_FILTER = True  # Active le filtre XSS du navigateur
SECURE_SSL_REDIRECT = False  # Change à True si le site utilise HTTPS

# Configuration de la gestion des erreurs CSRF
CSRF_FAILURE_VIEW = 'astroapp.views.csrf_failure'


# Configuration de l'envoi d'emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tepi.djet.neheh@gmail.com'
EMAIL_HOST_PASSWORD = 'sycz mlyq xvxc kfzr'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',  # Affiche uniquement INFO et niveaux supérieurs
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',  # Affiche uniquement les erreurs critiques de Django
            'propagate': False,
        },
        'astroapp': {
            'handlers': ['console'],
            'level': 'INFO',  # Désactive DEBUG par défaut pour votre application
            'propagate': False,
        },
    },
}








