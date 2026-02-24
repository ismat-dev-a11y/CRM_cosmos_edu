import os
from pathlib import Path
from datetime import timedelta
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv

load_dotenv()


# STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
# STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
    "16.16.92.30",
    "cosmos-edu.duckdns.org",
    "localhost",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "https://cosmos-edu.duckdns.org",
]

AUTH_USER_MODEL = "users.UserProfile"
ASGI_APPLICATION = "config.asgi.application"

DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "channels",
]
LOCAL_APPS = [
    "apps.core",
    "apps.courses",
    "apps.enrollments",
    "apps.groups",
    "apps.main",
    "apps.notifications",
    "apps.payments",
    "apps.ratings",
    "apps.tasks",
    "apps.users",
    # "apps.logs",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CORS_ALLOWED_ORIGINS = [
    "http://cosmos-edu.duckdns.org",
    "https://cosmos-edu.duckdns.org",
]
CORS_ALLOW_ALL_ORIGINS = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Training CRM API",
    "DESCRIPTION": "Production-grade CRM API for training centers",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6380)],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# logging

# LOG_DIR = BASE_DIR / "logs"
# LOG_DIR.mkdir(exist_ok=True)

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{asctime} {levelname} {name} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "file": {
#             "level": "INFO",  # DEBUG emas, balki INFO yoki WARNING
#             "class": "logging.FileHandler",
#             "filename": str(LOG_DIR / "debug.log"),
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",  # DEBUG emas, balki INFO yoki WARNING
#             "propagate": False,
#         },
#     },
# }


FRONTEND_PASSWORD_RESET_URL = "http://localhost:3000/reset-password"


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
