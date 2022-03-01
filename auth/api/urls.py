from django.urls.conf import path

from .views import (
    ChangePasswordView,
    ForgotPasswordView,
    LoginView,
    LogoutView,
    RegisterView,
)

app_name = "auth"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("forgot", ForgotPasswordView.as_view(), name="forgot-password"),
    path("change", ChangePasswordView.as_view(), name="change-password"),
]
