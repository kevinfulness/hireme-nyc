from django.shortcuts import render, redirect
from blog.models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def blog_index(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html", {
            "posts": posts
        })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
        })

@login_required
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
            "post": post,
            }
    return render(request, "blog/detail.html", context)