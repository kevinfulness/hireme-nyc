# blog/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('work/', views.blog_work, name="blog_work"),
]
