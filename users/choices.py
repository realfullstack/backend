from django.db import models
from django.utils.translation import gettext as _

import pytz


class UserStatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    SUSPENDED = "suspended", _("Suspended")


class UserTypeChoices(models.TextChoices):
    USER = "user", _("User")
    ADMIN = "admin", _("Admin")


def get_default_user_type_choices():
    return [UserTypeChoices.USER]


class UserLanguageChoices(models.TextChoices):
    ENGLISH = "en", _("English")
    SPANISH = "es", _("Spanish")


USER_TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
