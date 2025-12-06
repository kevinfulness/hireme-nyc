"""
Management command to verify CSS files are accessible from S3.
"""
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Verify CSS files are accessible from S3'

    def handle(self, *args, **options):
        self.stdout.write('Verifying CSS files on S3...\n')
        
        css_files = ['index.css', 'work.css', 'style.css']
        
        for css_file in css_files:
            try:
                # Get the URL from staticfiles storage
                url = staticfiles_storage.url(css_file)
                self.stdout.write(f'Checking: {css_file}')
                self.stdout.write(f'  URL: {url}')
                
                # Try to fetch the file
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Accessible ({len(response.content)} bytes)'))
                else:
                    self.stdout.write(self.style.ERROR(f'  ✗ Not accessible (Status: {response.status_code})'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error: {str(e)}'))
        
        self.stdout.write('\nTo verify in browser:')
        self.stdout.write('1. View page source and check <link> tags')
        self.stdout.write('2. Open browser DevTools > Network tab')
        self.stdout.write('3. Reload page and check CSS file URLs')
        self.stdout.write('4. URLs should point to: https://[bucket].s3.amazonaws.com/static/')

