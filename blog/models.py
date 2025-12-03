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
