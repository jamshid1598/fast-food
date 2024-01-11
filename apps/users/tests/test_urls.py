from django.urls import reverse, resolve
from django.test import SimpleTestCase

from user.api.views import user

# Create your tests here.


class UrlsTest(SimpleTestCase):
    
    def test_app_name(self):
        self.assertEquals(resolve("/users/api/").app_name, "user:user-api")

    def test_users_list(self):
        path = reverse("users:api:users-list")
        self.assertEquals(resolve(path).func.view_class, user.UsersList)
        self.assertNotEquals(
            resolve(path).func.view_class, user.UsersDetailUpdateDelete
        )

    def test_user_profile(self):
        path = reverse("users:api:profile")
        self.assertEquals(resolve(path).func.view_class, user.UserProfile)
        self.assertNotEquals(resolve(path).func.view_class, user.UsersList)

    def test_login(self):
        path = reverse("users:api:login")
        self.assertEquals(resolve(path).func.view_class, user.Login)
        self.assertNotEquals(resolve(path).func.view_class, user.Register)

    def test_register(self):
        path = reverse("users:api:register")
        self.assertEquals(resolve(path).func.view_class, user.Register)
        self.assertNotEquals(resolve(path).func.view_class, user.Login)

    def test_verify_otp(self):
        path = reverse("users:api:verify-otp")
        self.assertEquals(resolve(path).func.view_class, user.VerifyOtp)
        self.assertNotEquals(resolve(path).func.view_class, user.Login)

    def test_change_two_step_password(self):
        path = reverse("users:api:change-two-step-password")
        self.assertEquals(resolve(path).func.view_class, user.ChangeTwoStepPassword)
        self.assertNotEquals(resolve(path).func.view_class, user.CreateTwoStepPassword)

    def test_create_two_step_password(self):
        path = reverse("users:api:create-two-step-password")
        self.assertEquals(resolve(path).func.view_class, user.CreateTwoStepPassword)
        self.assertNotEquals(resolve(path).func.view_class, user.ChangeTwoStepPassword)

    def test_delete_account(self):
        path = reverse("users:api:delete-account")
        self.assertEquals(resolve(path).func.view_class, user.DeleteAccount)
        self.assertNotEquals(resolve(path).func.view_class, user.Register)

    def test_users_detail_update_delete(self):
        path = reverse("users:api:users-detail", args=[1])
        self.assertEquals(resolve(path).func.view_class, user.UsersDetailUpdateDelete)
        self.assertNotEquals(resolve(path).func.view_class, user.UsersList)
