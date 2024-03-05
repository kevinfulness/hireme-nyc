from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.title
