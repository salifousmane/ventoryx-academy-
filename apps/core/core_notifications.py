"""
Système de notifications — Ventoryx Academy
Architecture professionnelle : email, in-app, journal, multi-canal.
Conforme aux CGU, Politique de confidentialité et Mentions légales.
Version corrigée et complète.
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
SITE_URL = 'https://ventoryx-academy.com'


def _envoyer(email_destinataire, sujet, corps_texte):
    """Envoi email transactionnel."""
    try:
        send_mail(
            subject=sujet,
            message=corps_texte,
            from_email=FROM_EMAIL,
            recipient_list=[email_destinataire],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Erreur envoi email à {email_destinataire}: {str(e)}")


def _notifier(utilisateur, titre, message, notification_type='info', lien=''):
    """Crée une notification in-app."""
    try:
        from apps.messaging.models import Notification
        Notification.objects.create(
            destinataire=utilisateur,
            type=notification_type,
            titre=titre,
            message=message,
            lien=lien,
        )
    except Exception as e:
        logger.error(f"Erreur création notification pour {utilisateur}: {str(e)}")


def _notifier_dg(titre, message, notification_type='info'):
    """Notifie la Direction Générale."""
    from apps.users.models import User
    dgs = User.objects.filter(role='dg', is_active=True)
    for dg in dgs:
        _notifier(dg, titre, message, notification_type)
        _envoyer(dg.email, titre, message)


def _notifier_equipe(departement, titre, message, notification_type='info'):
    """Notifie tous les membres d'un département."""
    from apps.users.models import User
    membres = User.objects.filter(departement=departement, is_active=True)
    for membre in membres:
        _notifier(membre, titre, message, notification_type)
        if getattr(membre, 'email_notifications', True):
            _envoyer(membre.email, titre, message)


def _formule(user):
    """Retourne la formule d'abonnement en texte lisible."""
    if user.is_dg or user.is_coordinateur or user.is_gestionnaire:
        return 'Accès administration'
    if getattr(user, 'is_welcome_tier_1', False):
        return 'Offre Bienvenue — 365 jours offerts'
    if getattr(user, 'is_welcome_tier_2', False):
        return 'Offre Bienvenue — 30 jours offerts'
    try:
        sub = user.subscription
        if sub.est_active():
            return sub.get_plan_type_display()
    except Exception:
        pass
    return 'Formule Gratuite'


# ============================================================
# 1. AUTHENTIFICATION & SÉCURITÉ
# ============================================================

def bienvenue(user):
    """Email + notification de bienvenue après inscription."""
    sujet = "Bienvenue sur Ventoryx Academy"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre compte est activé. Bienvenue parmi nous.\n\n"
        f"Formule : {_formule(user)}\n\n"
        f"Connectez-vous pour commencer : {SITE_URL}/auth/login/\n\n"
        f"Si vous avez la moindre question, notre équipe est joignable par email. "
        f"Nous répondons sous 48 heures.\n\n"
        f"À très bientôt,\n"
        f"La Direction\n"
        f"Ventoryx Academy\n"
        f"{SITE_URL}"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Bienvenue à bord", "Votre compte est activé. Commencez votre formation.", 'succes')


def verification_email(user, code):
    """Vérification d'adresse email."""
    sujet = "Vérification de votre adresse email"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Pour vérifier votre adresse email, utilisez le code suivant : {code}\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


def reinitialisation_mot_de_passe(user, lien):
    """Lien de réinitialisation du mot de passe."""
    sujet = "Réinitialisation de votre mot de passe"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Vous avez demandé la réinitialisation de votre mot de passe.\n\n"
        f"Pour définir un nouveau mot de passe, cliquez sur ce lien : {lien}\n\n"
        f"Si vous n'êtes pas à l'origine de cette demande, ignorez ce message.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


def mot_de_passe_modifie(user):
    """Confirmation de changement de mot de passe."""
    sujet = "Votre mot de passe a été modifié"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Le mot de passe de votre compte Ventoryx Academy a été modifié.\n\n"
        f"Si vous n'êtes pas à l'origine de cette modification, "
        f"contactez immédiatement notre support.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


def nouvel_appareil(user, ip, navigateur):
    """Alerte connexion depuis un nouvel appareil."""
    sujet = "Nouvelle connexion détectée"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Une connexion à votre compte a été détectée depuis un nouvel appareil.\n\n"
        f"Adresse IP : {ip}\n"
        f"Navigateur : {navigateur}\n\n"
        f"Si vous n'êtes pas à l'origine de cette connexion, "
        f"modifiez immédiatement votre mot de passe.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


def connexion_suspecte(user, ip):
    """Alerte connexion suspecte."""
    sujet = "Tentative de connexion suspecte"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Une tentative de connexion suspecte a été détectée sur votre compte.\n\n"
        f"Adresse IP : {ip}\n\n"
        f"Si vous n'êtes pas à l'origine de cette tentative, contactez le support.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier_dg(f"Connexion suspecte - {user.email}", f"IP: {ip}", 'avertissement')


def compte_verrouille(user):
    """Notification compte temporairement verrouillé."""
    sujet = "Compte temporairement verrouillé"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre compte a été temporairement verrouillé suite à plusieurs "
        f"tentatives de connexion échouées.\n\n"
        f"Veuillez patienter 15 minutes avant de réessayer.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


def suppression_compte_demandee(user):
    """Confirmation demande suppression de compte."""
    sujet = "Demande de suppression de compte"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Nous avons bien reçu votre demande de suppression de compte.\n\n"
        f"Conformément au RGPD, vos données seront supprimées sous 30 jours.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier_dg(f"Suppression de compte - {user.email}", "Délai RGPD : 30 jours", 'avertissement')


def export_donnees(user):
    """Confirmation export de données (RGPD)."""
    sujet = "Export de vos données personnelles"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre demande d'export de données a été traitée.\n\n"
        f"Vous recevrez un fichier contenant l'ensemble de vos données "
        f"personnelles sous 30 jours.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


# ============================================================
# 2. FORMATION & APPRENTISSAGE
# ============================================================

def parcours_debloque(user, parcours_nom):
    """Notification quand un parcours est débloqué."""
    _notifier(user, "Nouveau parcours disponible",
              f"Le parcours \"{parcours_nom}\" est maintenant accessible.", 'info')


def quiz_reussi(user, quiz_titre, score):
    """Notification quiz réussi."""
    _notifier(user, "Quiz réussi",
              f"\"{quiz_titre}\" validé — Score : {score}%", 'succes')


def quiz_echoue(user, quiz_titre, score):
    """Notification quiz échoué."""
    _notifier(user, "Quiz à retenter",
              f"\"{quiz_titre}\" — Score : {score}% (minimum 70%)", 'avertissement')


def test_global_reussi(user, parcours_nom, score):
    """Notification test global réussi."""
    _notifier(user, "Test global réussi",
              f"\"{parcours_nom}\" validé — {score}%", 'succes')


def progression_hebdomadaire(user, parcours_nom, progression, temps_passe):
    """Résumé progression hebdomadaire."""
    sujet = f"Votre progression cette semaine — {parcours_nom}"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Cette semaine sur \"{parcours_nom}\" :\n"
        f"- Progression : +{progression}%\n"
        f"- Temps de formation : {temps_passe}\n\n"
        f"Continuez sur votre lancée.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)


# ============================================================
# 3. CERTIFICATION & VALIDATION
# ============================================================

def certificat_delivre(user, parcours_nom, numero_serie, hash_sha256):
    """Notification certificat délivré."""
    sujet = f"Félicitations ! Votre certificat \"{parcours_nom}\" est disponible"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Félicitations ! Vous venez de valider le parcours \"{parcours_nom}\".\n\n"
        f"Votre certificat :\n"
        f"- Numéro de série : {numero_serie}\n"
        f"- Empreinte SHA-256 : {hash_sha256}\n\n"
        f"Ce document est vérifiable publiquement : {SITE_URL}/verification-certificat/\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Certificat délivré",
              f"\"{parcours_nom}\" — N° {numero_serie}", 'succes',
              f'{SITE_URL}/verification-certificat/')
    _notifier_dg(f"Certificat délivré - {user.email}", f"Parcours : {parcours_nom}")


def certificat_verifie(numero_serie):
    """Log quand un certificat est vérifié publiquement."""
    _notifier_dg("Vérification certificat", f"Certificat {numero_serie} vérifié publiquement.")


def certificat_revoque(user, parcours_nom, raison):
    """Notification certificat révoqué."""
    sujet = f"Certificat \"{parcours_nom}\" révoqué"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre certificat \"{parcours_nom}\" a été révoqué.\n\n"
        f"Motif : {raison}\n\n"
        f"Contactez le support pour plus d'informations.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Certificat révoqué", f"\"{parcours_nom}\" — {raison}", 'avertissement')


# ============================================================
# 4. SUPPORT & CONTACT
# ============================================================

def ticket_cree(utilisateur, ticket_id, sujet_ticket):
    """Confirmation création ticket support."""
    _notifier(utilisateur, "Ticket créé", f"#{ticket_id} — \"{sujet_ticket}\"", 'info')
    _notifier_equipe('support', f"Nouveau ticket #{ticket_id}", sujet_ticket)


def ticket_repondu(utilisateur, ticket_id):
    """Notification réponse au ticket."""
    _notifier(utilisateur, "Réponse à votre ticket",
              f"Le ticket #{ticket_id} a reçu une réponse.", 'succes')


def ticket_resolu(utilisateur, ticket_id):
    """Notification ticket résolu."""
    _notifier(utilisateur, "Ticket résolu", f"Le ticket #{ticket_id} a été résolu.", 'succes')


def nouveau_message_contact(nom, email, categorie, sujet):
    """Alerte nouveau message de contact."""
    _notifier_equipe(categorie, f"Nouveau message — {sujet}", f"De : {nom} ({email})")


# ============================================================
# 5. SUPERVISION TECHNIQUE
# ============================================================

def bug_critique_signalé(departement, description, signale_par):
    """Alerte bug critique."""
    _notifier_equipe(departement, "Bug critique signalé",
                     f"Par : {signale_par}\nDescription : {description}", 'urgence')
    _notifier_dg(f"Bug critique — {departement}",
                 f"Signalé par : {signale_par}\n{description}", 'urgence')


def incident_serveur(service, statut):
    """Alerte incident serveur."""
    _notifier_dg(f"Incident serveur — {service}",
                 f"Statut : {statut}\nDate : {timezone.now().strftime('%d/%m/%Y %H:%M')}",
                 'critique')


def sauvegarde_reussie():
    """Notification sauvegarde réussie."""
    _notifier_dg("Sauvegarde réussie",
                 f"Sauvegarde quotidienne effectuée le {timezone.now().strftime('%d/%m/%Y à %H:%M')}.",
                 'info')


def sauvegarde_echouee(erreur):
    """Alerte sauvegarde échouée."""
    _notifier_dg("Échec sauvegarde",
                 f"La sauvegarde quotidienne a échoué : {erreur}",
                 'critique')


def maintenance_programmee(date_debut, date_fin):
    """Notification maintenance programmée."""
    from apps.users.models import User
    users = User.objects.filter(is_active=True, email_notifications=True)
    for user in users:
        _notifier(user, "Maintenance programmée",
                  f"Du {date_debut} au {date_fin}. La plateforme sera temporairement indisponible.",
                  'info')


# ============================================================
# 6. ADMINISTRATION INTERNE
# ============================================================

def nouveau_coordinateur(utilisateur, departement):
    """Notification ajout coordinateur."""
    _notifier(utilisateur, "Rôle Coordinateur",
              f"Vous êtes coordinateur du département {departement}.", 'succes')
    _notifier_dg(f"Nouveau coordinateur - {utilisateur.email}",
                 f"Département : {departement}")


def nouveau_gestionnaire(utilisateur, departement):
    """Notification ajout gestionnaire."""
    _notifier(utilisateur, "Rôle Gestionnaire",
              f"Vous êtes gestionnaire du département {departement}.", 'succes')


def utilisateur_suspendu(utilisateur, raison):
    """Notification suspension."""
    _notifier(utilisateur, "Compte suspendu",
              f"Votre compte a été suspendu. Motif : {raison}", 'avertissement')
    _notifier_dg(f"Utilisateur suspendu - {utilisateur.email}", f"Motif : {raison}", 'avertissement')


# ============================================================
# 7. FINANCES & ABONNEMENTS
# ============================================================

def paiement_confirme(user, montant, plan):
    """Confirmation de paiement."""
    sujet = "Paiement confirmé"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre paiement de {montant}€ pour l'abonnement {plan} a bien été reçu.\n\n"
        f"Votre abonnement est maintenant actif.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Paiement confirmé", f"Abonnement {plan} activé.", 'succes')


def paiement_echoue(user, raison):
    """Alerte paiement échoué."""
    sujet = "Paiement échoué"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre paiement n'a pas pu être traité.\n\n"
        f"Raison : {raison}\n\n"
        f"Veuillez mettre à jour vos informations de paiement.\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Paiement échoué", raison, 'avertissement')


def abonnement_expire(user):
    """Notification abonnement expiré."""
    sujet = "Votre abonnement a expiré"
    corps = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre abonnement est arrivé à expiration.\n\n"
        f"Votre compte repasse en formule Gratuite. "
        f"Vous conservez l'accès aux 2 parcours gratuits.\n\n"
        f"Pour retrouver l'accès à tous les parcours, "
        f"renouvelez votre abonnement : {SITE_URL}/premium/\n\n"
        f"Ventoryx Academy"
    )
    _envoyer(user.email, sujet, corps)
    _notifier(user, "Abonnement expiré", "Votre compte est repassé en formule Gratuite.", 'info')


# ============================================================
# 8. COMMUNAUTÉ & ÉVÉNEMENTS
# ============================================================

def palier_utilisateurs_atteint(nombre):
    """Notification palier d'inscriptions atteint."""
    _notifier_dg(f"{nombre} inscriptions atteintes",
                 f"La plateforme a atteint {nombre} utilisateurs inscrits.",
                 'succes')


def nouveau_partenariat(nom, email):
    """Notification nouveau partenariat."""
    _notifier_dg("Nouveau partenariat", f"{nom} ({email})", 'succes')
