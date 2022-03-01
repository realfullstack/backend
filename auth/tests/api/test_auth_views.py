from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory
from users.models import User


class UsersViewsTests(APITestCase):

    def test_register(self):
        response = self.client.post(
            reverse("api:auth:register"),
            {
                "name": "newuser",
                "email": "newuser@gmail.com",
                "password": "p1Q2W$word",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.json())
        self.assertIsNotNone(User.objects.filter(email="newuser@gmail.com").first())

    def test_bad_register(self):
        user = UserFactory()
        response = self.client.post(
            reverse("api:auth:register"),
            {"name": "newuser", "email": user.email, "password": "p1Q2W$word"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("auth.api.views.handle_forgot_password")
    def test_forgot(self, mock):
        # check bad email
        response = self.client.post(
            reverse("api:auth:forgot-password"), {"email": "newuser@gmail.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # check existing email
        user = UserFactory()
        response = self.client.post(
            reverse("api:auth:forgot-password"), {"email": user.email}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock.assert_called_once()

    @patch("auth.api.serializers.handle_reset_password")
    def test_change(self, mock):
        password = "p1Q2W$word"
        user = UserFactory()
        mock.return_value = user
        # change password
        response = self.client.post(
            reverse("api:auth:change-password"),
            {
                "new_password": password,
                "code": "AB-abcd",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("auth.api.serializers.handle_reset_password")
    def test_change_wrong(self, mock):
        password = "p1Q2W$word"
        mock.return_value = None
        # change password with bad token
        response = self.client.post(
            reverse("api:auth:change-password"),
            {
                "new_password": password,
                "code": "AB-abcd",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
