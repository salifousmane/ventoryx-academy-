from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Forum, Topic, Post

@require_http_methods(["GET"])
def forum_list(request):
    """List all forums"""
    forums = Forum.objects.filter(is_active=True)
    return render(request, 'forum/forum_principal.html', {'forums': forums})

@require_http_methods(["GET"])
def topic_detail(request, topic_id):
    """View topic"""
    topic = Topic.objects.get(id=topic_id)
    posts = topic.posts.all()
    return render(request, 'forum/sujet.html', {'topic': topic, 'posts': posts})