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


@login_required
def envoyer_dg(request):
    """Envoie un message à la Direction Générale."""
    if request.method == 'POST':
        from apps.users.models import User
        message_text = request.POST.get('message', '').strip()
        departement = request.POST.get('departement', request.user.departement if hasattr(request.user, 'departement') else '')
        if message_text:
            dg_users = User.objects.filter(role='dg', is_active=True)
            for dg in dg_users:
                Notification.objects.create(
                    destinataire=dg,
                    titre=f'Message de {request.user.get_full_name() or request.user.email} ({departement})',
                    message=message_text,
                    type='information',
                )
            from django.contrib import messages as dj_messages
            dj_messages.success(request, 'Message envoyé à la Direction.')
        else:
            from django.contrib import messages as dj_messages
            dj_messages.error(request, 'Le message ne peut pas être vide.')
    from django.shortcuts import redirect
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def envoyer_coordinateur(request):
    """Envoie un message au coordinateur du département."""
    if request.method == 'POST':
        from apps.users.models import User
        message_text = request.POST.get('message', '').strip()
        departement = request.POST.get('departement', '')
        if message_text:
            coords = User.objects.filter(role='coordinateur', is_active=True)
            if departement:
                coords = coords.filter(departement=departement)
            for coord in coords:
                Notification.objects.create(
                    destinataire=coord,
                    titre=f'Message de {request.user.get_full_name() or request.user.email}',
                    message=message_text,
                    type='information',
                )
            from django.contrib import messages as dj_messages
            dj_messages.success(request, 'Message envoyé au coordinateur.')
        else:
            from django.contrib import messages as dj_messages
            dj_messages.error(request, 'Le message ne peut pas être vide.')
    from django.shortcuts import redirect
    return redirect(request.META.get('HTTP_REFERER', '/'))
