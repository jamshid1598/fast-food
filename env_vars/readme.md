env_vars/
    |- .env
    |- .db


## .env
SECRET_KEY="9i9jy#(gdi+26q%j81ez*e4*e-^(&ca3b8(57rf-d+ysecir"
DEBUG=True
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_USER="db_admin"
DB_NAME="fastfood_db"
DB_PASSWORD="fastfood_12345"
DB_PORT=5432
DB_HOST="db"

SETTINGS="config.settings.dev"

SERVER_DOMAIN="127.0.0.1"
CSRF_COOKIE_DOMAIN="127.0.0.1:8000"

ESKIZ_EMAIL=""
ESKIZ_PASSWORD=""

REDIS_HOST="redis"
REDIS_PORT=6379

## .db
POSTGRES_USER="db_admin"
POSTGRES_PASSWORD="fastfood_12345"
POSTGRES_DB="fastfood_db"
