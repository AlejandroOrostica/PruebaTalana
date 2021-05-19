import time  # The defaul python odule for make db sleep

from django.db import connections  # Check db available
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand  # Allow create command


class Command(BaseCommand):
    """Django command to pause execution until db is available"""
    # Handle is what is ran whenever this management command is ran
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Database not yet available!'))
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(self.style.WARNING('Waiting...'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
