PROJECT_ROOT:=.

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  install    to install dependencies at system level"
.PHONY: help


install:
	sudo pipenv install --system --dev
.PHONY: install


lock:
	pipenv lock
.PHONY: lock

lint:
	black -v .
	isort -v  .
.PHONY: lint-fix

lint-check:
	flake8 --config .flake8 .
	black --check .
	isort --check-only .
.PHONY: lint-check

test:
	python manage.py test --keep
.PHONY: test

urls:
	python manage.py show_urls
.PHONY: urls

mypy:
	mypy --config-file mypy.ini  auth
.PHONY: mypy

coverage:
	coverage erase
	coverage run -a --rcfile=.coveragerc manage.py test --keep --no-input
	coverage xml
	coverage report
.PHONY: coverage

run:
	python manage.py runserver 0.0.0.0:8000
.PHONY: run

run-celery:
	celery -A config.celery worker --loglevel=debug -n 1
.PHONY: run-celery

migrate:
	python manage.py migrate
.PHONY: migrate

migrations:
	python manage.py makemigrations
.PHONY: migrations

provision:
	python manage.py utils_provision_infra --celery_vhost --database_name
.PHONY: provision

reset:
	python manage.py utils_reset_infra --celery_vhost --database_name
.PHONY: reset

make-messages:
	python manage.py makemessages -l es
.PHONY: make-messages

compile-messages:
	python manage.py compilemessages -l es
.PHONY: make-messages
