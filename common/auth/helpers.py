from django.conf import settings
from django.contrib.auth import login as django_auth_login
from django.contrib.auth import logout as django_auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.middleware.csrf import rotate_token
from django.shortcuts import redirect
from django.utils import translation
from django.utils.encoding import force_bytes, iri_to_uri
from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from cms.choices import EmailTemplateIDsChoices
from common.auth.jwt import token_for_user
from common.request.urls import add_url_params, get_url_domain
from users.models import User
from cms.tasks import send_user_email


def handle_forgot_password(request, user):
    code = "-".join(
        [
            urlsafe_base64_encode(force_bytes(user.pk)),
            default_token_generator.make_token(user),
        ]
    )
    email_context = {"forgot_url_params": {"code": code}}
    send_user_email(user.id, EmailTemplateIDsChoices.USER_AUTH_FORGOT, email_context)
    rotate_token(request)


def handle_reset_password(uidb64, token):
    try:
        uidb64 = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uidb64)
        if not default_token_generator.check_token(user, token):
            raise ValueError("Failed checking the user token")
        return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise ValueError("Failed checking the user token")

