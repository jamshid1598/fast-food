### [Fast-Food]

### docker commands

- `docker-compose -f dc-dev.yml build`
- `docker-compose -f dc-dev.yml up -d`
- `docker-compose -f dc-dev.yml logs -f`
- `docker-compose -f dc-dev.yml run --rm backend python manage.py migrate`
- `docker-compose -f dc-dev.yml run --rm backend python manage.py makemigrations`
- `docker-compose -f dc-dev.yml run --rm backend python manage.py createsuperuser`
- `docker-compose -f dc-dev.yml run --rm backend python manage.py test`


## dumpdata and loaddata

- _export data to fixture file_ `docker-compose -f dc-dev.yml run --rm backend python3 manage.py dumpdata <app>.<model> --indent 4 > apps/<app>/fixtures/<filename>.json`
- _import data from fixture file_ `docker-compose -f dc-prod.yml run --rm backend python3 manage.py loaddata apps/<app>/fixtures/<filename>.json`


