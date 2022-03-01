import json
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

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
        python manage.py utils_reset_infra --celery_vhost --database_name
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--celery_vhost",
            help="Delete the celery vhost exists",
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
            help="Delete the database name exists",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if settings.ENVIRONMENT in ["prod", "production"]:
            raise CommandError("This command should not be run in production")

        if options["celery_vhost"]:
            self.delete_vhost(options)
        if options["database_name"]:
            self.delete_database(options)

    def delete_vhost(self, options):
        VHOSTINFO = settings.CELERY_BROKER_URL
        rest_port = options["celery_vhost_port"]
        match = re.split(
            r"([^:]+)://([^@]+):([^@]+)@([^:]+):(\d+)/((\w){0,})", VHOSTINFO
        )
        if not match:
            raise Exception("Failed to parse rabbitmq connection")

        _, _, username, password, host, port, vhost, *_ = match
        self.stdout.write(f"Checking if '{vhost}' vhost exists")

        base_url = f"http://{host}:{rest_port}/api"

        session = requests.Session()
        session.auth = (username, password)
        session.headers.update({"Content-Type": "application/json"})

        r = session.get(f"{base_url}/vhosts/{vhost}")

        if r.status_code == 200:
            self.stdout.write("Vhost found, deleting")
            r = session.delete(
                f"{base_url}/vhosts/{vhost}",
                data=json.dumps({"name": vhost}),
            )
            if r.status_code == 204:
                self.stdout.write("Vhost deleted")
            else:
                self.stdout.write("Failed to delete or no 204 response received")
        elif r.status_code == 404:
            self.stdout.write("Vhost does not exists")
        else:
            r.raise_for_status()

    def delete_database(self, options):
        DBINFO = settings.DATABASES["default"]
        self.stdout.write(f"Checking if '{DBINFO['NAME']}' database exists")
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

            if row:
                self.stdout.write("Database found, trying to drop")
                cur.execute(
                    sql.SQL("DROP DATABASE {} WITH (FORCE)").format(
                        sql.Identifier(DBINFO["NAME"])
                    )
                )
                self.stdout.write("Database dropped")
            else:
                self.stdout.write("Database does not exist")
