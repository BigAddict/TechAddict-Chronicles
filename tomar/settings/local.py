from tomar.settings.base import *

INSTALLED_APPS += [
    "debug_toolbar",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
