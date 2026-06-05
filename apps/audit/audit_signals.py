"""Signaux d'audit pour les événements système."""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.conf import settings
from .models import AuditLog


def _get_ip_from_request(request):
    """Récupère l'IP depuis la requête."""
    if not request:
        return ''
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


@receiver(user_logged_in)
def log_connexion(sender, request, user, **kwargs):
    """Journalise une connexion réussie."""
    AuditLog.objects.create(
        utilisateur=user,
        action='connexion',
        objet=f'Connexion de {user.email}',
        ip_address=_get_ip_from_request(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255] if request else '',
    )


@receiver(user_logged_out)
def log_deconnexion(sender, request, user, **kwargs):
    """Journalise une déconnexion."""
    if user:
        AuditLog.objects.create(
            utilisateur=user,
            action='deconnexion',
            objet=f'Déconnexion de {user.email}',
            ip_address=_get_ip_from_request(request),
        )


@receiver(user_login_failed)
def log_echec_connexion(sender, credentials, request, **kwargs):
    """Journalise un échec de connexion."""
    AuditLog.objects.create(
        action='echec_connexion',
        gravite='avertissement',
        objet=f'Tentative échouée pour: {credentials.get("username", "inconnu")}',
        ip_address=_get_ip_from_request(request),
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def log_creation_utilisateur(sender, instance, created, **kwargs):
    """Journalise la création d'un compte utilisateur."""
    if created:
        AuditLog.objects.create(
            utilisateur=instance,
            action='creation',
            objet=f'Création compte: {instance.email}',
            description=f'Rôle: {instance.role}',
        )
        if getattr(instance, 'is_welcome_tier_1', False):
            AuditLog.objects.create(
                utilisateur=instance,
                action='bienvenue_1',
                gravite='critique',
                objet=f'Offre bienvenue #1 à {instance.email}',
            )
        elif getattr(instance, 'is_welcome_tier_2', False):
            AuditLog.objects.create(
                utilisateur=instance,
                action='bienvenue_2',
                objet=f'Offre bienvenue #2 à {instance.email}',
            )


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def log_suppression_utilisateur(sender, instance, **kwargs):
    """Journalise la suppression d'un compte utilisateur."""
    AuditLog.objects.create(
        action='suppression',
        gravite='critique',
        objet=f'Suppression compte: {instance.email}',
        description='Action nécessitant validation secondaire',
    )
