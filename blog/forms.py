# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['image', 'image2', 'image3', 'image4', 'image5']
