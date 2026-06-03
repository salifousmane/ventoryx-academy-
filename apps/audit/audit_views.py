"""Consultation du journal d'audit. Réservé DG."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.users.decorators import dg_required
from .models import AuditLog


@login_required
@dg_required
def journal_audit(request):
    """Affiche le journal d'audit avec filtres."""
    logs = AuditLog.objects.select_related('utilisateur').all()

    # Filtres
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action=action)

    gravite = request.GET.get('gravite')
    if gravite:
        logs = logs.filter(gravite=gravite)

    utilisateur_id = request.GET.get('utilisateur')
    if utilisateur_id and utilisateur_id.isdigit():
        logs = logs.filter(utilisateur_id=int(utilisateur_id))

    date_debut = request.GET.get('date_debut')
    if date_debut:
        logs = logs.filter(timestamp__date__gte=date_debut)

    date_fin = request.GET.get('date_fin')
    if date_fin:
        logs = logs.filter(timestamp__date__lte=date_fin)

    # Pagination
    paginator = Paginator(logs, 50)
    page = request.GET.get('page', 1)
    logs_page = paginator.get_page(page)

    return render(request, 'audit/journal.html', {
        'logs': logs_page,
        'actions': AuditLog.ACTION_CHOICES,
        'gravites': AuditLog.GRAVITE_CHOICES,
        'filtre_action': action,
        'filtre_gravite': gravite,
        'filtre_utilisateur': utilisateur_id,
    })
