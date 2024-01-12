from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase

from datetime import timedelta

# Create your tests here.


class UserTest(TestCase):
    
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            phone="998991231122",
            first_name="test-user-first-name",
            last_name="test-user-last-name",
        )
        self.superuser = get_user_model().objects.create_superuser(
            phone="998991231122",
            first_name="test-superuser-first-name",
            last_name="test-superuser-last-name",
        )

    def test_str_method(self):
        self.assertEquals(str(self.user), self.user.phone)
        self.assertEquals(str(self.superuser), self.superuser.phone)

    def test_get_full_name(self):
        self.assertEqual(
            self.user.get_full_name, f"{self.user.first_name} {self.user.last_name}"
        )
        self.assertEqual(
            self.superuser.get_full_name,
            f"{self.superuser.first_name} {self.superuser.last_name}",
        )
        self.assertNotEqual(self.superuser.get_full_name, f"{self.superuser.phone}")

    def test_model_manager_for_set_password(self):
        self.assertFalse(self.user.has_usable_password())
        self.assertFalse(self.superuser.has_usable_password())
