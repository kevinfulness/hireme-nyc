"""
Management command to collect only CSS files to S3.

This is a lightweight alternative to collectstatic that only collects CSS files.
Useful when DISABLE_COLLECTSTATIC is set but you still need CSS files updated.
"""
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import get_finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Collect only CSS files to static storage (S3)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_true',
            help='Do not prompt for user input.',
        )

    def handle(self, *args, **options):
        self.stdout.write('Collecting CSS files only...\n')
        
        # Use the staticfiles storage (which is S3 in production)
        destination_storage = staticfiles_storage
        
        # Find all CSS files
        css_files = []
        for finder in get_finders():
            for path, storage in finder.list(['']):
                if path.endswith('.css'):
                    css_files.append((path, storage))
        
        if not css_files:
            self.stdout.write(self.style.WARNING('No CSS files found.'))
            return
        
        self.stdout.write(f'Found {len(css_files)} CSS file(s):')
        for path, storage in css_files:
            self.stdout.write(f'  - {path}')
        
        # Collect each CSS file
        collected_count = 0
        for path, storage in css_files:
            try:
                # Open the file from source storage
                with storage.open(path) as source_file:
                    # Save to destination storage (S3)
                    saved_path = destination_storage.save(path, source_file)
                    collected_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Collected: {path} -> {saved_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to collect {path}: {str(e)}'))
        
        self.stdout.write(f'\n{self.style.SUCCESS(f"Successfully collected {collected_count} CSS file(s).")}')

