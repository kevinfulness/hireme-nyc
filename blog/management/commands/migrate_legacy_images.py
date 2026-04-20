"""
Management command to migrate legacy image fields to the new Media model.

This command:
1. Finds all Posts with legacy image URLs (image, image2, image3, image4, image5)
2. Downloads each image from the URL
3. Creates a Media object for each image
4. Preserves the order based on field position
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from blog.models import Post, Media
import os
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from django.db.models import Max


class Command(BaseCommand):
    help = 'Migrate legacy image fields (image, image2, etc.) to the new Media model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually creating Media objects',
        )
        parser.add_argument(
            '--clear-legacy',
            action='store_true',
            help='Clear legacy image fields after successful migration',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        clear_legacy = options['clear_legacy']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        posts = Post.objects.all()
        total_posts = posts.count()
        migrated_count = 0
        error_count = 0
        
        self.stdout.write(f'Found {total_posts} posts to process...\n')
        
        for post in posts:
            legacy_images = []
            image_fields = ['image', 'image2', 'image3', 'image4', 'image5']
            
            # Collect all non-empty image URLs with their positions
            for index, field_name in enumerate(image_fields):
                image_url = getattr(post, field_name, None)
                if image_url and image_url.strip():
                    legacy_images.append({
                        'url': image_url.strip(),
                        'position': index + 1,
                        'field_name': field_name
                    })
            
            if not legacy_images:
                continue
            
            self.stdout.write(f'Processing post: {post.title} ({len(legacy_images)} images)')
            
            # Get the highest position for existing media
            max_position = Media.objects.filter(post=post).aggregate(
                max_pos=Max('position')
            )['max_pos'] or 0
            
            for img_data in legacy_images:
                url = img_data['url']
                position = max_position + img_data['position']
                
                try:
                    if dry_run:
                        self.stdout.write(f'  [DRY RUN] Would migrate: {url} -> position {position}')
                        continue
                    
                    # Download the image
                    req = Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0')
                    with urlopen(req, timeout=30) as response:
                        # Get filename from URL or generate one
                        parsed_url = urlparse(url)
                        filename = os.path.basename(parsed_url.path)
                        if not filename or '.' not in filename:
                            # Generate filename based on content type or default
                            content_type = response.headers.get('content-type', '')
                            if 'image' in content_type:
                                ext = content_type.split('/')[-1].split(';')[0]
                                filename = f'legacy_image_{post.id}_{img_data["position"]}.{ext}'
                            else:
                                filename = f'legacy_image_{post.id}_{img_data["position"]}.jpg'
                        
                        # Ensure filename is unique in the media/ directory
                        file_path = f'media/{filename}'
                        if default_storage.exists(file_path):
                            name, ext = os.path.splitext(filename)
                            file_path = f'media/{name}_{post.id}_{img_data["position"]}{ext}'
                        
                        # Read and save the file
                        file_content = ContentFile(response.read())
                        saved_path = default_storage.save(file_path, file_content)
                    
                    # Create Media object
                    media = Media.objects.create(
                        post=post,
                        file=saved_path,
                        position=position
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Migrated: {url} -> {saved_path} (position {position})'))
                    
                except (URLError, HTTPError) as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Failed to download {url}: {str(e)}'))
                    error_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error processing {url}: {str(e)}'))
                    error_count += 1
            
            # Clear legacy fields if requested and migration was successful
            if clear_legacy and not dry_run:
                for field_name in image_fields:
                    setattr(post, field_name, None)
                post.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Cleared legacy image fields for {post.title}'))
            
            migrated_count += 1
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Migration complete!'))
        self.stdout.write(f'Posts processed: {migrated_count}/{total_posts}')
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'Errors encountered: {error_count}'))
        if dry_run:
            self.stdout.write(self.style.WARNING('This was a dry run. Run without --dry-run to perform migration.'))

