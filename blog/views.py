from django.shortcuts import render, redirect
from blog.models import Post, Brand
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def blog_index(request):
    posts = Post.objects.all()
    brands = Brand.objects.all().order_by('position')
    login_form = AuthenticationForm() if not request.user.is_authenticated else None
    return render(request, "blog/index.html", {
        "posts": posts,
        "brands": brands,
        'form': login_form,
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
def blog_work(request):
    posts = Post.objects.all()
    return render(request, "blog/work.html", {
        "posts": posts
    })
    
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
            "post": post,
            }
    return render(request, "blog/detail.html", context)

def brand_detail(request, slug):
    brand = Brand.objects.get(slug=slug)
    posts = brand.posts.all()
    brands = Brand.objects.filter(posts__isnull=False).distinct()
    context = {
        "brand": brand,
        "posts": posts,
        "brands": brands,
    }
    return render(request, "blog/brand_detail.html", context)