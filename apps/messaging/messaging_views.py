"""Vues : contact, newsletter, notifications."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from apps.users.decorators import gestionnaire_required, dg_required
from .models import MessageContact, Notification, NewsletterInscription


def contact(request):
    """Formulaire de contact (redirige vers core:contact)."""
    return redirect('core:contact')


@require_POST
def newsletter_inscription(request):
    """Inscription à la newsletter."""
    email = request.POST.get('email', '').strip()
    source = request.POST.get('source', '')
    if email:
        obj, created = NewsletterInscription.objects.get_or_create(email=email, defaults={'source': source})
        return JsonResponse({'ok': True, 'created': created})
    return JsonResponse({'ok': False, 'error': 'Email requis'}, status=400)


@login_required
def mes_notifications(request):
    """API retournant les notifications de l'utilisateur."""
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date_creation')[:50]
    non_lues = notifications.filter(est_lue=False).count()
    
    data = {
        'notifications': [
            {
                'id': n.id,
                'type': n.type,
                'titre': n.titre,
                'message': n.message,
                'lien': n.lien,
                'est_lue': n.est_lue,
                'date': n.date_creation.isoformat(),
            } for n in notifications
        ],
        'non_lues': non_lues,
    }
    return JsonResponse(data)


@login_required
@require_POST
def marquer_notification_lue(request, notification_id):
    """Marque une notification comme lue."""
    notif = Notification.objects.filter(id=notification_id, destinataire=request.user).first()
    if notif and not notif.est_lue:
        notif.est_lue = True
        notif.date_lecture = timezone.now()
        notif.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=404)


@login_required
@require_POST
def marquer_tout_lu(request):
    """Marque toutes les notifications comme lues."""
    Notification.objects.filter(destinataire=request.user, est_lue=False).update(
        est_lue=True, date_lecture=timezone.now()
    )
    return JsonResponse({'ok': True})


@login_required
@dg_required
def messages_contact(request):
    """Liste tous les messages de contact (réservé DG)."""
    messages_list = MessageContact.objects.select_related('traite_par').order_by('-date_envoi')
    return render(request, 'messaging/contact_list.html', {'messages': messages_list})


@login_required
def inbox(request):
    """Page messagerie."""
    return render(request, 'messaging/inbox.html', {'page_title': 'Messagerie'})


@login_required
@gestionnaire_required
def envoyer_dg(request):
    """Envoie un message à la Direction Générale."""
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if message:
            from apps.users.models import User
            dgs = User.objects.filter(role='dg', is_active=True)
            for dg in dgs:
                Notification.objects.create(
                    destinataire=dg,
                    type='info',
                    titre=f'Message de {request.user.get_full_name()} ({request.user.departement})',
                    message=message,
                )
            messages.success(request, 'Message envoyé à la Direction.')
        return redirect(request.META.get('HTTP_REFERER', 'core:index'))
    return redirect('core:index')


@login_required
@gestionnaire_required
def envoyer_equipe(request):
    """Envoie un message à l'équipe du même département."""
    if request.method == 'POST':
        departement = request.POST.get('departement', request.user.departement)
        message = request.POST.get('message', '').strip()
        if message:
            from apps.users.models import User
            equipe = User.objects.filter(departement=departement, is_active=True)
            for membre in equipe:
                if membre != request.user:
                    Notification.objects.create(
                        destinataire=membre,
                        type='info',
                        titre=f'Message équipe {departement}',
                        message=message,
                    )
            messages.success(request, 'Message envoyé à l\'équipe.')
        return redirect(request.META.get('HTTP_REFERER', 'core:index'))
    return redirect('core:index')


@login_required
@gestionnaire_required
def envoyer_coordinateur(request):
    """Envoie un message au coordinateur du département."""
    if request.method == 'POST':
        departement = request.POST.get('departement', request.user.departement)
        message = request.POST.get('message', '').strip()
        if message:
            from apps.users.models import User
            coord = User.objects.filter(role='coordinateur', departement=departement, is_active=True).first()
            if coord:
                Notification.objects.create(
                    destinataire=coord,
                    type='info',
                    titre=f'Message de {request.user.get_full_name()}',
                    message=message,
                )
                messages.success(request, 'Message envoyé au coordinateur.')
            else:
                messages.error(request, 'Aucun coordinateur trouvé pour ce département.')
        return redirect(request.META.get('HTTP_REFERER', 'core:index'))
    return redirect('core:index')
