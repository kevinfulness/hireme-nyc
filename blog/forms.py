# blog/forms.py
from django import forms
from multiupload.fields import MultiFileField
from .models import Post, Video

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['image', 'image2', 'image3', 'image4', 'image5']

class VideoUploadForm(forms.Form):
    videos = MultiFileField(
        min_num=0,
        max_num=100,
        max_file_size=1024*1024*500,  # 500MB max per file
        required=False,
    )
