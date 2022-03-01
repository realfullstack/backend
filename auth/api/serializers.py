import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from common.auth.helpers import handle_reset_password
from common.auth.jwt import token_for_user
from users.models import User


class UserTokenSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        return token_for_user(user)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        "duplicate_email": _("Another user with the same email already exists"),
    }

    def validate_email(self, email):
        if email and User.objects.filter(email__iexact=email).exists():
            self.fail("duplicate_email")
        return email

    def validate_password(self, password):
        try:
            validate_password(password, None)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.error_list[0].message)
        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    default_error_messages = {
        "invalid_credentials": _("Invalid email and password combination"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        self.user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if self.user:
            attrs["token"] = token_for_user(self.user)
            return attrs

        self.fail("invalid_credentials")


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    default_error_messages = {
        "invalid_email": _("The email entered is not associated with any account"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        email = attrs.get("email").lower()
        self.user = User.objects.filter(email=email).first()
        if self.user:
            return attrs
        self.fail("invalid_email")


class CheckChangePasswordTokenSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    default_error_messages = {
        "invalid_token": _("Invalid token"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate_code(self, code):
        if match := re.search("^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$", code):
            uidb64 = match.group("uidb64")
            token = match.group("token")
            try:
                user = handle_reset_password(uidb64, token)
                if not user:
                    self.fail("invalid_token")
            except ValueError:
                self.fail("invalid_token")
        else:
            self.fail("invalid_token")

        self.user = user


class ChangePasswordTokenSerializer(CheckChangePasswordTokenSerializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, password):
        try:
            validate_password(password, None)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.error_list[0].message)
        return password
