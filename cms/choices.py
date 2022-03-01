from django.db import models


class EmailTemplateIDsChoices(models.TextChoices):
    USER_AUTH_WELCOME = "user_auth_welcome", "User Signup Welcome"
    USER_AUTH_FORGOT = "user_auth_forgot", "User Forgot Password"
