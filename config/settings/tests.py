import os
from django.test import TestCase


SECRET_KEY_INSECURE_PREFIX = "django-insecure-"
SECRET_KEY_MIN_LENGTH = 50
SECRET_KEY_MIN_UNIQUE_CHARACTERS = 5


def _check_secret_key(secret_key):
    print("\n\nSECRET_KEY check ...")
    print(f"⚙️ unique chars min len 5: {list(set(secret_key))[:5]} ", len(set(secret_key)) >= SECRET_KEY_MIN_UNIQUE_CHARACTERS)
    print(f"⚙️ secret key min len: {len(secret_key)} ", len(secret_key) >= SECRET_KEY_MIN_LENGTH)
    print("⚙️ not added insecure prefix 'django-insecure-': ", not secret_key.startswith(SECRET_KEY_INSECURE_PREFIX))
    print("done ...\n\n")
    return (
        len(set(secret_key)) >= SECRET_KEY_MIN_UNIQUE_CHARACTERS and
        len(secret_key) >= SECRET_KEY_MIN_LENGTH and not
        secret_key.startswith(SECRET_KEY_INSECURE_PREFIX)
    )


class TestCredentials(TestCase):
    def test_secret_key_strength(self):
        secret_key = os.environ.get('SECRET_KEY')
        self.assertTrue(_check_secret_key(secret_key))
