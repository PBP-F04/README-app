ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ARG DATABASE_URL
ARG SECRET_KEY
ARG DJANGO_SETTINGS_MODULE
ARG PRODUCTION

ENV DATABASE_URL=$DATABASE_URL
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
ENV PRODUCTION=$PRODUCTION


RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "README.wsgi"]