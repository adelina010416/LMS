from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input('Email: ')
        password = input('Password: ')
        user = User.objects.create(
            email=email,
            first_name='Adelina',
            last_name='Zimina',
            is_staff=False,
            is_superuser=False
        )
        user.set_password(password)
        user.save()
