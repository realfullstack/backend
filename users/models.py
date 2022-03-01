import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields.citext import CIEmailField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from annoying.fields import AutoOneToOneField

from common.models import AutoDateTimeMixin

from .choices import (
    USER_TIMEZONE_CHOICES,
    UserLanguageChoices,
    UserStatusChoices,
    UserTypeChoices,
    get_default_user_type_choices,
)
from .managers import UserManager


class BaseUserSlim(AbstractBaseUser, PermissionsMixin):
    username = None
    last_login = None

    name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Name"),
    )
    email = CIEmailField(
        max_length=128,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("Email"),
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        abstract = True


class User(BaseUserSlim):
    status = models.CharField(
        max_length=32,
        choices=UserStatusChoices.choices,
        null=False,
        default=UserStatusChoices.ACTIVE,
    )
    types = ArrayField(
        models.CharField(
            max_length=32,
            choices=UserTypeChoices.choices,
            null=False,
        ),
        default=get_default_user_type_choices,
        size=len(UserTypeChoices.choices),
    )

    class Meta:
        db_table = "users"
        ordering = ("-id",)


class UserInfo(AutoDateTimeMixin, models.Model):
    user = AutoOneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="info",
        null=False,
        primary_key=True,
    )
    timezone = models.CharField(
        default="UTC",
        choices=USER_TIMEZONE_CHOICES,
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("Timezone"),
    )
    language = models.CharField(
        default=UserLanguageChoices.ENGLISH,
        choices=UserLanguageChoices.choices,
        max_length=2,
        null=True,
        blank=True,
        verbose_name=_("Language"),
    )
    join_at = models.DateTimeField(null=True)

    @property
    def language_is_custom(self):
        return self.language and self.language != UserLanguageChoices.ENGLISH

    class Meta:
        db_table = "users_info"
        ordering = ("-user_id",)
