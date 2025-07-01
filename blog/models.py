from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class Post(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    year = models.CharField(max_length=4, null=True)
    company = models.CharField(max_length=255, null=True)
    logo = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    surface = models.CharField(max_length=255, null=True)
    body = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
