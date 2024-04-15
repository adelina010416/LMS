from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@mail.ru',
            first_name='',
            last_name='',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('1310')
        user.save()
