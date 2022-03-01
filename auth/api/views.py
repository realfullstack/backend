from django.contrib.auth import logout as django_auth_logout
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api.mixins import AtomicMixin, PostViewMixin
from common.api.permissions import IsNotAuthenticated
from common.auth.helpers import handle_forgot_password
from users.models import User

from .serializers import (
    ChangePasswordTokenSerializer,
    CheckChangePasswordTokenSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserTokenSerializer,
)


class LoginView(PostViewMixin, GenericAPIView):
    """Login a user."""

    permission_classes = (IsNotAuthenticated,)
    serializer_class = LoginSerializer

    def execute(self, serializer):
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(AtomicMixin, PostViewMixin, GenericAPIView):
    """Register a new user."""

    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer

    def execute(self, serializer):
        new_user = User.objects.create_user(
            serializer.data["email"],
            serializer.data["password"],
            name=serializer.data["name"],
        )
        new_user.is_active = True
        new_user.save()
        return Response(
            UserTokenSerializer(new_user).data, status=status.HTTP_201_CREATED
        )


class ForgotPasswordView(PostViewMixin, GenericAPIView):
    """Forgot a password."""

    permission_classes = (IsNotAuthenticated,)
    serializer_class = ForgotPasswordSerializer

    def execute(self, serializer):
        user = serializer.user
        handle_forgot_password(self.request, user)

        return Response(_("Email Sent"), status=status.HTTP_200_OK)


class ChangePasswordView(PostViewMixin, RetrieveAPIView, GenericAPIView):
    """Change a password."""

    permission_classes = (IsNotAuthenticated,)
    serializer_class = ChangePasswordTokenSerializer

    def execute(self, serializer):
        user = serializer.user
        user.set_password(serializer.data["new_password"])
        user.save()

        return Response(_("Password changed"), status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        data = request.query_params
        serializer = CheckChangePasswordTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(_("Valid"), status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout a user."""

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        django_auth_logout(request)
        return Response(_("Logged out"), status=status.HTTP_200_OK)
