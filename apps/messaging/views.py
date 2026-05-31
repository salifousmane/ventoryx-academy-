from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Message, Notification

@require_http_methods(["GET"])
def inbox(request):
    """View user inbox"""
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/inbox.html', {'messages': messages})

@require_http_methods(["GET"])
def contact_list(request):
    """View contact list"""
    return render(request, 'messaging/contact_list.html')