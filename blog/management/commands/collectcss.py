"""
Management command to collect only CSS files to S3.

This is a lightweight alternative to collectstatic that only collects CSS files.
Useful when DISABLE_COLLECTSTATIC is set but you still need CSS files updated.
Uses boto3 directly to ensure exact filenames without any hashing or versioning.
"""
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import get_finders
from django.conf import settings
import boto3
import os


class Command(BaseCommand):
    help = 'Collect only CSS files to static storage (S3) with exact filenames'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_true',
            help='Do not prompt for user input.',
        )

    def handle(self, *args, **options):
        self.stdout.write('Collecting CSS files only...\n')
        
        # Initialize S3 client
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to initialize S3 client: {str(e)}'))
            return
        
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
        
        # Collect each CSS file directly to S3 with exact filename
        collected_count = 0
        for path, storage in css_files:
            try:
                # Open and read the file from source storage
                with storage.open(path) as source_file:
                    file_content = source_file.read()
                
                # Upload directly to S3 with exact filename (no hashing)
                key = f'static/{path}'
                
                # Delete existing file if it exists
                try:
                    s3_client.delete_object(Bucket=bucket_name, Key=key)
                except:
                    pass  # File might not exist, that's okay
                
                # Upload with exact name
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=key,
                    Body=file_content,
                    ContentType='text/css',
                    ACL='public-read'
                )
                
                collected_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Collected: {path} -> s3://{bucket_name}/{key}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to collect {path}: {str(e)}'))
        
        self.stdout.write(f'\n{self.style.SUCCESS(f"Successfully collected {collected_count} CSS file(s).")}')

