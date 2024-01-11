import os
import dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
dotenv.read_dotenv(os.path.join(base_dir, 'env_vars', '.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('SETTINGS'))

application = get_wsgi_application()
