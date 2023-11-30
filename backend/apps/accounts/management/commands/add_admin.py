# yourapp/management/commands/create_demo_superuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a demo superuser for development purposes'

    def handle(self, *args, **options):
        if not get_user_model().objects.filter(email='admin@example.com').exists():
            get_user_model().objects.create_superuser('admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Demo superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Demo superuser already'))

