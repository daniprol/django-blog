import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if none exists"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Specifies the username for the superuser.")
        parser.add_argument("--email", type=str, help="Specifies the email for the superuser.")
        parser.add_argument("--password", type=str, help="Specifies the password for the superuser.")

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            username = options.get("username") or os.environ.get("DJANGO_SUPERUSER_USERNAME")
            email = options.get("email") or os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = options.get("password") or os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            if username and email and password:
                call_command("createsuperuser", username=username, email=email, password=password, interactive=False)
                self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
            else:
                self.stdout.write(self.style.ERROR("Superuser not created. Missing required arguments."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists."))
