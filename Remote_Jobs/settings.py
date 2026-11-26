import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)

# Configuración local: usa un secreto propio mediante .env antes de desplegar.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-clave-local-solo-desarrollo-no-usar-en-produccion",
)
RENDER = os.environ.get("RENDER", "").lower() == "true"
DEBUG = os.environ.get("DJANGO_DEBUG", "False" if RENDER else "True").lower() in {"1", "true", "yes"}
if RENDER and DEBUG:
    raise ValueError("DJANGO_DEBUG debe ser False en Render.")
_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
ALLOWED_HOSTS = [host.strip() for host in _hosts.split(",") if host.strip()]
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if render_host:
    ALLOWED_HOSTS.append(render_host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "App_Remote_Jobs.apps.AppRemoteJobsConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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
        "App_Remote_Jobs.context_processors.contexto_favoritos",
    ]},
}]

WSGI_APPLICATION = "Remote_Jobs.wsgi.application"
ASGI_APPLICATION = "Remote_Jobs.asgi.application"

# SQLite mantiene los datos de desarrollo en un archivo local reconstruible con migraciones.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
database_url = os.environ.get("DATABASE_URL", "").strip()
if database_url:
    DATABASES["default"] = dj_database_url.parse(database_url, conn_max_age=60, conn_health_checks=True)
if RENDER and DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":
    raise ValueError("Configura DATABASE_URL con PostgreSQL antes de desplegar en Render.")

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
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Tipo de clave primaria aplicado a los modelos que no declaran una explícitamente.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
# En Render las fotos locales son temporales y pueden perderse al reiniciar.

# El correo de consola es solo para desarrollo, nunca para enlaces de producción.
brevo_api_key = os.environ.get("BREVO_API_KEY", "").strip()
email_backend_default = (
    "django.core.mail.backends.console.EmailBackend" if DEBUG
    else "django.core.mail.backends.dummy.EmailBackend"
)
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", email_backend_default)
if brevo_api_key:
    EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
    ANYMAIL = {"BREVO_API_KEY": brevo_api_key}
if not DEBUG and EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
    raise ValueError("No uses el backend de consola para correo de producción.")
PASSWORD_RESET_ENABLED = EMAIL_BACKEND != "django.core.mail.backends.dummy.EmailBackend"
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "True").lower() in {"1", "true", "yes"}
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "Remote Jobs <no-reply@remotejobs.local>")

AUTHENTICATION_BACKENDS = [
    "App_Remote_Jobs.backends.AutenticacionCorreoONombreUsuario",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:profile"
LOGOUT_REDIRECT_URL = "jobs:inicio"

ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = False
# La vinculación requiere iniciar sesión en la cuenta existente.
SOCIALACCOUNT_EMAIL_AUTHENTICATION = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = False
GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "").strip()
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "").strip()
SOCIALACCOUNT_PROVIDERS = {"google": {"SCOPE": ["openid", "profile", "email"], "AUTH_PARAMS": {"access_type": "online"}, "OAUTH_PKCE_ENABLED": True, "FETCH_USERINFO": True}}
if GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET:
    SOCIALACCOUNT_PROVIDERS["google"]["APPS"] = [{"client_id": GOOGLE_OAUTH_CLIENT_ID, "secret": GOOGLE_OAUTH_CLIENT_SECRET, "key": ""}]

SOCIALACCOUNT_ADAPTER = "App_Remote_Jobs.adapters.AdaptadorCuentaSocialRemoteJobs"

X_CONTENT_TYPE_OPTIONS = "nosniff"
X_FRAME_OPTIONS = "DENY"

# Las cookies solo pueden exigirse por HTTPS cuando la instalación lo utiliza.
if not DEBUG:
    if SECRET_KEY.startswith("django-insecure-") or SECRET_KEY == "replace-with-a-local-secret":
        raise ValueError("Define una DJANGO_SECRET_KEY segura para producción.")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    if RENDER:
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
        SECURE_SSL_REDIRECT = True
        SECURE_HSTS_SECONDS = 3600
