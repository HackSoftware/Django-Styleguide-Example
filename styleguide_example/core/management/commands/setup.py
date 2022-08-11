from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """
    This is the core setup command, that calls other setup sub-commands.
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        call_command("setup_users")
