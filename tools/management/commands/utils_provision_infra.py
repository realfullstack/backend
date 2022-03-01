import json
import re

from django.conf import settings
from django.core.management.base import BaseCommand

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # <-- ADD THIS LINE
import requests


class Command(BaseCommand):
    requires_system_checks = False
    requires_migrations_checks = False
    """
Create missing databases

    Example:
        python manage.py utils_provision_infra --celery_vhost --database_name
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--celery_vhost",
            help="Create or ensure the celery vhost exists",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--celery_vhost_port",
            help="Custom port the management for celery API",
            default=15672,
        )
        parser.add_argument(
            "--database_name",
            help="Create or ensure the database name exists",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if options["celery_vhost"]:
            self.create_vhost(options)
        if options["database_name"]:
            self.create_database(options)

    def create_vhost(self, options):
        VHOSTINFO = settings.CELERY_BROKER_URL
        rest_port = options["celery_vhost_port"]
        match = re.split(
            r"([^:]+)://([^@]+):([^@]+)@([^:]+):(\d+)/((\w){0,})", VHOSTINFO
        )
        if not match:
            raise Exception("Failed to parse rabbitmq connection")

        _, _, username, password, host, port, vhost, *_ = match
        self.stdout.write(f"Checking if {vhost} vhost exists")

        base_url = f"http://{host}:{rest_port}/api"

        session = requests.Session()
        session.auth = (username, password)
        session.headers.update({"Content-Type": "application/json"})

        r = session.get(f"{base_url}/vhosts/{vhost}")

        if r.status_code == 404:
            self.stdout.write("Missing vhost")
            r = session.put(
                f"{base_url}/vhosts/{vhost}",
                data=json.dumps({"name": vhost}),
            )
            if r.status_code == 201:
                self.stdout.write("Vhost created")
            else:
                self.stdout.write("Failed to create or no 201 response received")
        elif r.status_code == 200:
            self.stdout.write("Vhost exists already")
        else:
            r.raise_for_status()

    def create_database(self, options):
        DBINFO = settings.DATABASES["default"]
        self.stdout.write(f"Checking if {DBINFO['NAME']} database exists")
        con = psycopg2.connect(
            user=DBINFO["USER"],
            host=DBINFO["HOST"],
            password=DBINFO["PASSWORD"],
        )

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cur:
            cur.execute(
                "SELECT * FROM pg_database WHERE datname=%s LIMIT 1",
                [DBINFO["NAME"]],
            )
            row = cur.fetchone()

            if not row:
                self.stdout.write("Database appears to be missing, creating db")
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DBINFO["NAME"]))
                )
                self.stdout.write("Database created")
            else:
                self.stdout.write("Database exists")
