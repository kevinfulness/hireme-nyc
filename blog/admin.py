from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm
from django.db.models import Max
from multiupload.fields import MultiFileField
import os
from blog.models import Post, Brand, Media

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    fields = ('file', 'position', 'media_preview', 'media_type')
    readonly_fields = ('media_preview', 'media_type')
    can_delete = True
    
    def media_preview(self, obj):
        if obj.pk and obj.file:
            if obj.is_video():
                return format_html(
                    '<video width="200" controls><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                    obj.file.url
                )
            else:
                return format_html(
                    '<img src="{}" width="200" style="max-height: 200px; object-fit: contain;" />',
                    obj.file.url
                )
        return "No media uploaded"
    media_preview.short_description = 'Preview'
    
    def media_type(self, obj):
        if obj.pk:
            return 'Video' if obj.is_video() else 'Image'
        return '-'
    media_type.short_description = 'Type'

class PostAdminForm(ModelForm):
    media_files = MultiFileField(
        min_num=0,
        max_num=100,
        max_file_size=1024*1024*500,  # 500MB max per file
        required=False,
    )
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['image', 'image2', 'image3', 'image4', 'image5']

class BrandAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    inlines = [MediaInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Handle multiple media uploads (images and videos)
        if 'media_files' in form.cleaned_data and form.cleaned_data['media_files']:
            # Get the highest position for existing media
            max_position = Media.objects.filter(post=obj).aggregate(
                max_pos=Max('position')
            )['max_pos'] or 0
            
            # Create Media objects for each uploaded file
            for index, uploaded_file in enumerate(form.cleaned_data['media_files']):
                Media.objects.create(
                    post=obj,
                    file=uploaded_file,
                    position=max_position + index + 1
                )

class MediaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'post', 'media_type_display', 'position', 'created_on')
    list_filter = ('post', 'created_on')
    search_fields = ('post__title',)
    
    def media_type_display(self, obj):
        return 'Video' if obj.is_video() else 'Image'
    media_type_display.short_description = 'Type'

admin.site.register(Brand, BrandAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)
