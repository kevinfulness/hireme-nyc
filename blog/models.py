from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, unique=True)
    body = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    headline = models.CharField(max_length=1024, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    year = models.CharField(max_length=4, null=True)
    role = models.CharField(max_length=255, null=True)
    surface = models.CharField(max_length=255, null=True)
    body = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    image2 = models.CharField(max_length=255, blank=True, null=True)
    image3 = models.CharField(max_length=255, blank=True, null=True)
    image4 = models.CharField(max_length=255, blank=True, null=True)
    image5 = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_all_media(self):
        """
        Returns a list of all media items (images and videos) in order.
        Each item is a dict with 'type' ('image' or 'video') and 'url' or 'file'.
        """
        media = []
        
        # Add legacy image fields (for backward compatibility)
        image_fields = ['image', 'image2', 'image3', 'image4', 'image5']
        for field_name in image_fields:
            image_url = getattr(self, field_name, None)
            if image_url:
                media.append({
                    'type': 'image',
                    'url': image_url,
                })
        
        # Add media items from Media model (ordered by position)
        for media_item in self.media_items.all():
            media.append({
                'type': 'video' if media_item.is_video() else 'image',
                'file': media_item.file,
                'url': media_item.file.url,
            })
        
        return media

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_items')
    file = models.FileField(upload_to='media/')
    created_on = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(default=0, help_text="Order in which media appears")
    
    # Video file extensions
    VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.wmv', '.m4v'}

    class Meta:
        ordering = ['position', 'created_on']
        verbose_name_plural = 'Media'

    def __str__(self):
        media_type = 'Video' if self.is_video() else 'Image'
        return f"{self.post.title} - {media_type} {self.id}"
    
    def is_video(self):
        """Check if this media file is a video based on file extension."""
        import os
        if self.file:
            file_ext = os.path.splitext(self.file.name)[1].lower()
            return file_ext in self.VIDEO_EXTENSIONS
        return False
    
    def is_image(self):
        """Check if this media file is an image."""
        return not self.is_video()
