from django.contrib import admin
from blog.models import Post, Brand

class BrandAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Brand, BrandAdmin)
admin.site.register(Post, PostAdmin)
