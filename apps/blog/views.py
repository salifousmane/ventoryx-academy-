from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import BlogPost, HelpArticle

@require_http_methods(["GET"])
def blog_list(request):
    """List all blog posts"""
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'pages/support/blog.html', {'posts': posts})

@require_http_methods(["GET"])
def blog_detail(request, slug):
    """View blog post"""
    post = BlogPost.objects.get(slug=slug)
    return render(request, 'pages/support/blog_detail.html', {'post': post})

@require_http_methods(["GET"])
def help_center(request):
    """Help center"""
    articles = HelpArticle.objects.filter(is_published=True)
    return render(request, 'pages/support/centre_aide.html', {'articles': articles})