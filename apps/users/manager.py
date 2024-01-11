from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('unique username must be required')

        password = extra_fields.pop('password', None)

        user = self.model(
            username=username,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, **extra_fields):
        return self._create_user(username, False, False, **extra_fields)

    def create_superuser(self, username, **extra_fields):
        return self._create_user(username, True, True, **extra_fields)
