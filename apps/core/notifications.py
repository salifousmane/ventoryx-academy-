import logging

logger = logging.getLogger(__name__)


def certificat_delivre(user, parcours_nom, numero, hash_sha):
    try:
        from apps.messaging.models import Notification
        Notification.objects.create(
            destinataire=user,
            titre='Certificat délivré !',
            message=f'Félicitations ! Votre certificat pour "{parcours_nom}" a été délivré. Numéro : {numero}',
            type='succes',
        )
    except Exception as e:
        logger.error(f"Erreur notification certificat: {e}")


def test_global_reussi(user, parcours_nom, score):
    try:
        from apps.messaging.models import Notification
        Notification.objects.create(
            destinataire=user,
            titre='Test global réussi !',
            message=f'Bravo ! Vous avez réussi le test global de "{parcours_nom}" avec {score}%.',
            type='succes',
        )
    except Exception as e:
        logger.error(f"Erreur notification test global: {e}")


def quiz_reussi(user, quiz_titre, score):
    try:
        from apps.messaging.models import Notification
        Notification.objects.create(
            destinataire=user,
            titre='Quiz réussi !',
            message=f'Bravo ! Vous avez réussi "{quiz_titre}" avec {score}%.',
            type='succes',
        )
    except Exception as e:
        logger.error(f"Erreur notification quiz: {e}")


def quiz_echoue(user, quiz_titre, score):
    try:
        from apps.messaging.models import Notification
        Notification.objects.create(
            destinataire=user,
            titre='Quiz non réussi',
            message=f'Vous avez obtenu {score}% pour "{quiz_titre}". Score minimum requis : 70%. Réessayez !',
            type='avertissement',
        )
    except Exception as e:
        logger.error(f"Erreur notification quiz échoué: {e}")
