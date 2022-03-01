import datetime

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

import jwt

from users.models import User

DEFAULT_EXPIRATION_TIME = 60 * 60 * 24


def token_decode(token):
    """
    decode token
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["exp"]},
    )


def token_encode(data, exp_time=DEFAULT_EXPIRATION_TIME):
    """
    create token
    """
    claims = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_time),
    }
    return jwt.encode(
        {**data, **claims},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def token_for_user(user):
    # !FIXME - reject the token based on the db password hash so that we still don't store it
    return token_encode(
        {
            "user_id": user.id,
            "name": user.name,
        }
    )


def get_user_from_data(request, data):
    if "user_id" in data:
        try:
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist:
            user = AnonymousUser()
        request._cached_user = user
    elif not hasattr(request, "_cached_user"):
        request._cached_user = user

    return request._cached_user
