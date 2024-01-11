env_vars/
    |- .env
    |- .db


## .env
SECRET_KEY=""
DEBUG=True
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_USER=""
DB_NAME=""
DB_PASSWORD=""
DB_PORT=5432
DB_HOST="db"

SETTINGS="config.settings.dev"

SERVER_DOMAIN="127.0.0.1"
CSRF_COOKIE_DOMAIN="127.0.0.1:8000"

## .db
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
