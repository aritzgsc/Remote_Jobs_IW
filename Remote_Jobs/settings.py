import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración local: usa un secreto propio mediante .env antes de desplegar.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-clave-local-solo-desarrollo-no-usar-en-produccion",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in {"1", "true", "yes"}
_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
ALLOWED_HOSTS = [host.strip() for host in _hosts.split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "App_Remote_Jobs.apps.AppRemoteJobsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Remote_Jobs.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "App_Remote_Jobs" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.template.context_processors.csrf",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "Remote_Jobs.wsgi.application"
ASGI_APPLICATION = "Remote_Jobs.asgi.application"

# SQLite mantiene los datos de desarrollo en un archivo local reconstruible con migraciones.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

# Validadores predeterminados de Django para evitar contraseñas demasiado simples.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Idioma de la interfaz y zona horaria usada para presentar fechas.
LANGUAGE_CODE = "es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True
# Archivos estáticos versionados y archivos subidos por usuarios tienen destinos distintos.
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Tipo de clave primaria aplicado a los modelos que no declaran una explícitamente.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

X_CONTENT_TYPE_OPTIONS = "nosniff"
X_FRAME_OPTIONS = "DENY"
