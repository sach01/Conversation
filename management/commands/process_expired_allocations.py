# maramari_app/management/commands/process_expired_allocations.py

from django.core.management.base import BaseCommand
from maramari_app.utils import handle_expired_allocations, unlock_timed_out_translations
from django.utils import timezone

class Command(BaseCommand):
    help = 'Process expired allocations and unlock timed-out translations.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Processing expired allocations...')
        handle_expired_allocations()
        unlock_timed_out_translations()
        self.stdout.write('Expired allocations processed successfully.')
