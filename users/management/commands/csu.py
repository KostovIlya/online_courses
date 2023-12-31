import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email=os.getenv('SUPERUSER_EMAIL'),
            first_name='admin',
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        if created:
            user.set_password(os.getenv('SUPERUSER_PASSWORD'))
            user.save()
