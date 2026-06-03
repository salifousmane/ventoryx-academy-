"""Tâches asynchrones Celery."""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task
def envoyer_notification_contact(nom, email, categorie, sujet, message):
    """Envoie un email au DG et notifie les gestionnaires."""
    from apps.users.models import User
    from apps.messaging.models import Notification
    
    # 1. Envoyer un seul email au DG
    dgs = User.objects.filter(role='dg', is_active=True)
    for dg in dgs:
        send_mail(
            subject=f'[Contact] {sujet}',
            message=f'De : {nom} ({email})\n\nMessage :\n{message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[dg.email],
            fail_silently=True,
        )
        logger.info(f"Email contact envoyé au DG {dg.email}")
    
    # 2. Notifier les gestionnaires du département concerné
    gestionnaires = User.objects.filter(role='gestionnaire', departement=categorie, is_active=True)
    for gestionnaire in gestionnaires:
        Notification.objects.create(
            destinataire=gestionnaire,
            type='info',
            titre=f'Nouveau message - {categorie}',
            message=f"De : {nom}\nSujet : {sujet}\n\n{message[:200]}...",
        )
        logger.info(f"Notification créée pour gestionnaire {gestionnaire.email}")


@shared_task
def backup_database():
    """Sauvegarde quotidienne."""
    import shutil
    from pathlib import Path
    
    try:
        if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            db_path = settings.DATABASES['default']['NAME']
            backup_dir = Path(settings.BASE_DIR) / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            date_str = timezone.now().strftime('%Y%m%d')
            backup_path = backup_dir / f'ventoryx_{date_str}.sqlite3'
            shutil.copy2(db_path, backup_path)
            logger.info(f"Sauvegarde SQLite créée: {backup_path}")
            
            for f in backup_dir.glob('ventoryx_*.sqlite3'):
                if f.stat().st_mtime < timezone.now().timestamp() - 7 * 86400:
                    f.unlink()
    except Exception as e:
        logger.error(f"Erreur backup_database: {str(e)}")


@shared_task
def nettoyer_comptes_inactifs():
    from apps.users.models import User
    
    date_limite = timezone.now() - timedelta(days=730)
    count = User.objects.filter(role='etudiant', last_login__lt=date_limite, is_active=True).update(is_active=False)
    logger.info(f"{count} comptes inactifs désactivés")
    return count


@shared_task
def archiver_messages_traites():
    from apps.messaging.models import MessageContact
    
    date_limite = timezone.now() - timedelta(days=30)
    count = MessageContact.objects.filter(statut='repondu', date_reponse__lt=date_limite).update(statut='archive')
    logger.info(f"{count} messages archivés")
    return count


@shared_task
def envoyer_relances_inactivite_7j():
    from apps.users.models import User
    from apps.parcours.models import ProgressionUtilisateur
    
    date_limite = timezone.now() - timedelta(days=7)
    etudiants = User.objects.filter(role='etudiant', is_active=True, last_login__lt=date_limite)
    
    count = 0
    for etudiant in etudiants:
        progression = ProgressionUtilisateur.objects.filter(user=etudiant).first()
        parcours_nom = progression.parcours.nom if progression else 'votre parcours'
        send_mail(
            subject=f'{etudiant.first_name}, votre cours vous attend',
            message=f'Bonjour {etudiant.first_name},\n\nCela fait une semaine que vous n\'avez pas avancé sur "{parcours_nom}".\n\nÀ votre rythme,\nL\'équipe Ventoryx Academy',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[etudiant.email],
            fail_silently=True,
        )
        count += 1
    return count


@shared_task
def envoyer_relances_inactivite_30j():
    from apps.users.models import User
    
    date_limite = timezone.now() - timedelta(days=30)
    etudiants = User.objects.filter(role='etudiant', is_active=True, last_login__lt=date_limite)
    
    count = 0
    for etudiant in etudiants:
        send_mail(
            subject=f'{etudiant.first_name}, on pense à vous',
            message=f'Bonjour {etudiant.first_name},\n\nVoilà 30 jours sans nouvelle. Votre compte est toujours actif.\n\nPrenez soin de vous,\nL\'équipe Ventoryx Academy',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[etudiant.email],
            fail_silently=True,
        )
        count += 1
    return count


@shared_task
def envoyer_rapport_hebdomadaire():
    from apps.users.models import User
    from apps.institution.models import Candidature, Certificat
    from apps.messaging.models import MessageContact
    
    dgs = User.objects.filter(role='dg', is_active=True)
    if not dgs:
        return
    
    now = timezone.now()
    debut_semaine = now - timedelta(days=7)
    
    inscriptions = User.objects.filter(date_joined__gte=debut_semaine).count()
    total_utilisateurs = User.objects.count()
    certificats = Certificat.objects.filter(date_delivrance__gte=debut_semaine).count()
    messages_recus = MessageContact.objects.filter(date_envoi__gte=debut_semaine).count()
    messages_en_attente = MessageContact.objects.filter(statut='non_lu').count()
    candidatures = Candidature.objects.filter(date_soumission__gte=debut_semaine).count()
    
    for dg in dgs:
        send_mail(
            subject=f'Rapport hebdomadaire',
            message=f'Inscriptions : {inscriptions}\nTotal utilisateurs : {total_utilisateurs}\nCertificats : {certificats}\nMessages reçus : {messages_recus} (dont {messages_en_attente} en attente)\nCandidatures : {candidatures}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[dg.email],
            fail_silently=True,
        )
    logger.info("Rapport hebdomadaire envoyé")
