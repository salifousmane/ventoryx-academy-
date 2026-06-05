from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MessageContact, Notification


@login_required
def inbox(request):
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date_creation')
    return render(request, 'messaging/inbox.html', {
        'notifications': notifications,
        'page_title': 'Notifications',
    })


@login_required
def contact_list(request):
    messages_list = MessageContact.objects.all().order_by('-date_envoi')
    return render(request, 'messaging/contact_list.html', {
        'messages': messages_list,
        'page_title': 'Messages de contact',
    })
