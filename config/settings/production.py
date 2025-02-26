import os

from dotenv import load_dotenv

from config.settings.base import *

# update environment variables for production
dotenv_path = os.path.join(BASE_DIR, ".env.production")
load_dotenv(dotenv_path)

DEBUG = False

ALLOWED_HOSTS = ["bigaddict.shop", "127.0.0.1", "www.bigaddict.shop"]

INSTALLED_APPS += ["anymail"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Anymail
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
# https://anymail.readthedocs.io/en/stable/esps/sendgrid/

EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
}

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


CSRF_TRUSTED_ORIGINS = ["https://*.bigaddict.shop"]


# Update database configuration from $DATABASE_URL.
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)
