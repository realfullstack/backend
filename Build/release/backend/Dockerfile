### base
FROM python:3.8.7-slim-buster as base

RUN apt-get update && apt-get install -y \
    bash \
    wait-for-it \
    make \
    curl \
    gettext \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup django \
    && mkdir /app \
    && useradd -g django --home /app django \
    && chown django:django /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_MAX_RETRIES=2
ENV PIPENV_KEEP_OUTDATED=true
ENV PIPENV_CACHE_DIR=/cache/pipenv
ENV PIP_CACHE_DIR=/cache/pip

RUN pip install pipenv==2020.11.15 --no-cache-dir

COPY ./Pipfile* /

RUN pipenv install --system --dev --deploy --clear\
    && pip uninstall pipenv -y \
    && rm -rf /cache
### base DONE


### main_dev
FROM base as main_dev

ARG BUILD_NUMBER
ARG BUILD_DATE

ENV BUILD_NUMBER=$BUILD_NUMBER
ENV BUILD_DATE=$BUILD_DATE
ENV DJANGO_SETTINGS_MODULE=config.settings

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app:$PYTHONPATH"

WORKDIR /app

COPY . /app

RUN python manage/static_dev.py collectstatic --no-input

# USER django

### main_dev DONE

### nginx
FROM nginx:1.19.6-alpine as nginx
COPY ./Build/release/backend/conf/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=main_dev /app/release/static /app/static
### nginx DONE
