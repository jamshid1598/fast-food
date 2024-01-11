# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gdal-bin libgdal-dev libpq-dev && apt-get install -y python3-gdal \
  && apt-get install -y binutils libproj-dev && apt-get install -y python-psycopg2

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

# copy project
COPY . .

RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

RUN adduser --disabled-password --no-create-home django

USER django

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/backend/entrypoint.sh"]
