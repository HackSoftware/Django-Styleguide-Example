from django.core.management.base import BaseCommand
from django.db import transaction

from styleguide_example.users.tests.factories import BaseUserFactory


class Command(BaseCommand):
    help = """
    This command sets up users for local development.

    You can use whatever suits you here.
    """

    objects_count = 1000

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print(f"Creating {self.objects_count} users ...")
        BaseUserFactory.create_batch(self.objects_count)
