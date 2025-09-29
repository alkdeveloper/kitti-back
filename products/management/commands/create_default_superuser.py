from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = "Create default superuser from .env variables if not exists"

    def handle(self, *args, **kwargs):
        username = settings.DJANGO_SUPERUSER_USERNAME
        password = settings.DJANGO_SUPERUSER_PASSWORD
        email = settings.DJANGO_SUPERUSER_EMAIL

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {username} already exists"))