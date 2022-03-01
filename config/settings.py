import logging
from pathlib import Path
import re
import sys

from django.utils.translation import ugettext_lazy as _

from corsheaders.defaults import default_headers
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.is_file():
    environ.Env.read_env(env_file=str(ENV_FILE))

env = environ.Env(DEBUG=(bool, False))

# Django core settings
BASE_DIR = BASE_DIR
DEBUG = env.bool("DEBUG", default=False)
LOGGING_LEVEL = env.int("LOGGING_LEVEL", default=logging.INFO)
CONSOLE_LOG_LEVEL = env.str("CONSOLE_LOG_LEVEL", default="INFO")
ENVIRONMENT = env.str("ENVIRONMENT")
IS_TEST = "test" in sys.argv

if IS_TEST:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    ENVIRONMENT = "test"

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=False)
BUILD_NUMBER = env.str("BUILD_NUMBER", default="N/A")
BUILD_DATE = env.str("BUILD_DATE", default="N/A")


SESSION_COOKIE_NAME = "_sid"


# Celery settings
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=None)
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {}
CELERY_TASK_ALWAYS_EAGER = False
if env.str("CELERY_VHOST", default=None):
    # replace the vhost
    CELERY_BROKER_URL = re.sub(
        r"([^:]+://[^@]+@[^:]+:\d+)/(\w){0,}",
        r"\1/" + env.str("CELERY_VHOST"),
        CELERY_BROKER_URL,
        0,
        re.DOTALL | re.MULTILINE,
    )

# Email settings
if env("EMAIL_URL", default=None):
    EMAIL_CONFIG = env.email_url("EMAIL_URL")
    vars().update(EMAIL_CONFIG)

EMAIL_DEFAULT_FROM_NAME = "RealFullStack"
EMAIL_DEFAULT_FROM_ADDRESS = "contact@realfullstack.com"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "common.drf.exceptions.exception_handler",
}


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "widget_tweaks",
    "rest_framework",  # utilities for rest apis
    "rest_framework.authtoken",  # token authentication
    "django_filters",
    "django_json_widget",
    "cacheops",
]

LOCAL_APPS = ["auth", "users", "tools"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.http.middleware.HeadersToRequestMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {},
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/auth/login"
LOGIN_REDIRECT_URL = "/users/dashboard"


JWT_SECRET_KEY = env("JWT_SECRET_KEY", default=SECRET_KEY)
JWT_ALGORITHM = "HS256"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": env.db_url("DATABASE_URL"),
}

if env.str("DATABASE_NAME", default=None):
    DATABASES["default"]["NAME"] = env.str("DATABASE_NAME")


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_COOKIE_NAME = "_lang"

LOCALE_PATHS = [
    str(BASE_DIR / "locale"),
]


LANGUAGES = (
    ("en", _("English")),
    ("es", _("Spanish")),
)

LANGUAGES_CODES = (
    "en",
    "es",
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    str(BASE_DIR / "static"),
]
STATIC_ROOT = str(BASE_DIR / "release/static")


MEDIA_ROOT = env.str("MEDIA_ROOT", default=str(BASE_DIR / "media"))
MEDIA_URL = env.str("MEDIA_URL", default="/media/")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": CONSOLE_LOG_LEVEL,
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "level": CONSOLE_LOG_LEVEL,
        "handlers": [
            "console",
        ],
    },
}

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3030',
# ] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    r"realfullstack\.com",
]
CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-authorization",
]

CACHEOPS_REDIS = env.str("CACHE_URL")
CACHEOPS_DEFAULTS = {"timeout": 24 * 60 * 60}
CACHEOPS = {}

if DEBUG:

    CORS_ORIGIN_ALLOW_ALL = True

    SHELL_PLUS_PRINT_SQL = True

    # Truncate sql queries to this number of characters (this is the default)
    SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

    # To disable truncation of sql queries use
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None

    # Specify sqlparse configuration options when printing sql queries to the console
    SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
        reindent_aligned=True,
        truncate_strings=500,
    )

    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
        "drf_yasg",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += [
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.AdminRenderer",
    ]
    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "rest_framework.schemas.coreapi.AutoSchema"

    def show_toolbar(request):
        return DEBUG and not IS_TEST

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

    SWAGGER_SETTINGS = {
        "LOGOUT_URL": "/auth/logout",
        "USE_SESSION_AUTH": True,
        "SECURITY_DEFINITIONS": {
            "Bearer": {
                "type": "apiKey",
                "name": "X-Authorization",
                "in": "header",
            },
        },
    }

    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(asctime)s %(levelname)s %(message)s",
    )

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


CSRF_USE_SESSIONS = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        release=f"{BUILD_NUMBER}-{BUILD_DATE}",
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            LoggingIntegration(level=logging.ERROR),
        ],
        send_default_pii=True,
    )

SITE_URL = env.str("SITE_URL", default="https://fluent.software")
