from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('connexion', 'Connexion'),
        ('deconnexion', 'Déconnexion'),
        ('inscription', 'Inscription'),
        ('modification_profil', 'Modification profil'),
        ('changement_mdp', 'Changement mot de passe'),
        ('reset_mdp', 'Réinitialisation mot de passe'),
        ('paiement', 'Paiement'),
        ('acces_vault', 'Accès vault'),
        ('chatbot', 'Chatbot'),
        ('chatbot_bloque', 'Chatbot bloqué'),
        ('chatbot_reponse_bloquee', 'Chatbot réponse bloquée'),
        ('module_cree', 'Module créé'),
        ('cours_cree', 'Cours créé'),
        ('quiz_cree', 'Quiz créé'),
        ('question_ajoutee', 'Question ajoutée'),
        ('tache_cree', 'Tâche créée'),
        ('bug_signale', 'Bug signalé'),
        ('campagne_cree', 'Campagne créée'),
        ('article_cree', 'Article créé'),
        ('ticket_cree', 'Ticket créé'),
        ('maquette_cree', 'Maquette créée'),
        ('composant_cree', 'Composant créé'),
        ('export_messages', 'Export messages'),
        ('export_candidatures', 'Export candidatures'),
        ('rapport_hebdo', 'Rapport hebdomadaire'),
        ('message_coordinateurs', 'Message coordinateurs'),
        ('archivage_messages', 'Archivage messages'),
        ('audit_departement', 'Audit département'),
        ('audit_lance', 'Audit lancé'),
        ('validation_budget', 'Validation budget'),
        ('formation_planifiee', 'Formation planifiée'),
        ('partenaire_ajoute', 'Partenaire ajouté'),
        ('innovation_proposee', 'Innovation proposée'),
        ('nc_signalée', 'Non-conformité signalée'),
        ('chat_envoye', 'Chat envoyé'),
        ('message_repondu', 'Message répondu'),
        ('autre', 'Autre'),
    ]

    GRAVITE_CHOICES = [
        ('info', 'Information'),
        ('avertissement', 'Avertissement'),
        ('critique', 'Critique'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='audit_logs',
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, default='autre')
    gravite = models.CharField(max_length=20, choices=GRAVITE_CHOICES, default='info')
    objet = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Journal d'audit"
        verbose_name_plural = "Journal d'audit"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} — {self.action} — {self.utilisateur}"
