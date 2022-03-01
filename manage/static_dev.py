from pathlib import Path
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    settings.configure(
        DEBUG=True,
        SECRET_KEY=get_random_secret_key(),
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "debug_toolbar",
            "django_extensions",
            "rest_framework",
        ],
        STATIC_URL="/static/",
        STATICFILES_DIRS=[
            str(BASE_DIR / "static"),
        ],
        STATIC_ROOT=str(BASE_DIR / "release/static"),
    ),

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
