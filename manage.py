#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
dotenv.read_dotenv(os.path.join(base_dir, 'env_vars', '.env'))


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('SETTINGS'))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()