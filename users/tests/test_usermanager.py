from django.test import TestCase

from users.factories import UserFactory
from users.models import User


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = UserFactory(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_user_has_info(self):
        user = UserFactory(email="normal@user.com", password="foo")
        self.assertIsNotNone(user.info)
