"""
Journal d'audit immutable.
Manifeste §2.2 : Inviolable, lecture seule, aucune suppression.
Manifeste §7.4 : Traçabilité des attributions.
Manifeste §B : Chaîne de hachage pour intégrité.
"""
from django.db import models
from djanaago.conf import settings
import hashlib


class AuditLog(models.Model):
    ACTION_CHOICES = [
        # Authentification & Sécurité
        ('connexion', 'Connexion'),
        ('deconnexion', 'Déconnexion'),
        ('echec_connexion', 'Échec de connexion'),
        ('compte_verrouille', 'Compte verrouillé'),
        ('nouvel_appareil', 'Nouvel appareil détecté'),
        ('connexion_suspecte', 'Connexion suspecte'),
        ('otp_verification', 'Vérification OTP'),
        ('validation_secondaire', 'Validation secondaire'),
        # Gestion des utilisateurs
        ('creation', 'Création de compte'),
        ('modification', 'Modification de compte'),
        ('suspension', 'Suspension de compte'),
        ('suppression', 'Suppression de compte'),
        ('activation', 'Activation de compte'),
        ('bienvenue_1', 'Offre bienvenue #1 (365j)'),
        ('bienvenue_2', 'Offre bienvenue #2 (30j)'),
        ('export_donnees', 'Export données personnelles'),
        # Formation & Apprentissage
        ('cours_debute', 'Cours débuté'),
        ('cours_termine', 'Cours terminé'),
        ('quiz_soumis', 'Quiz soumis'),
        ('quiz_reussi', 'Quiz réussi'),
        ('quiz_echoue', 'Quiz échoué'),
        ('test_global_soumis', 'Test global soumis'),
        ('test_global_reussi', 'Test global réussi'),
        ('test_global_echoue', 'Test global échoué'),
        # Certification & Validation
        ('certificat_delivre', 'Certificat délivré'),
        ('certificat_verifie', 'Certificat vérifié'),
        ('certificat_revoque', 'Certificat révoqué'),
        # Pédagogie
        ('module_cree', 'Module créé'),
        ('module_modifie', 'Module modifié'),
        ('module_archive', 'Module archivé'),
        ('cours_cree', 'Cours créé'),
        ('cours_modifie', 'Cours modifié'),
        ('quiz_cree', 'Quiz créé'),
        ('question_ajoutee', 'Question ajoutée'),
        ('question_modifiee', 'Question modifiée'),
        ('question_supprimee', 'Question supprimée'),
        ('message_traite', 'Message traité'),
        ('newsletter_envoyee', 'Newsletter envoyée'),
        # Technique
        ('tache_cree', 'Tâche créée'),
        ('tache_modifiee', 'Tâche modifiée'),
        ('tache_terminee', 'Tâche terminée'),
        ('bug_signale', 'Bug signalé'),
        ('bug_resolu', 'Bug résolu'),
        ('deploiement', 'Déploiement effectué'),
        ('maintenance_activee', 'Maintenance activée'),
        ('maintenance_desactivee', 'Maintenance désactivée'),
        # Marketing
        ('campagne_cree', 'Campagne créée'),
        ('campagne_modifiee', 'Campagne modifiée'),
        ('campagne_lancee', 'Campagne lancée'),
        ('campagne_arretee', 'Campagne arrêtée'),
        ('article_cree', 'Article créé'),
        ('article_publie', 'Article publié'),
        ('article_modifie', 'Article modifié'),
        ('post_reseaux', 'Publication réseaux sociaux'),
        ('newsletter_cree', 'Newsletter créée'),
        # Opérations
        ('formation_planifiee', 'Formation planifiée'),
        ('formation_modifiee', 'Formation modifiée'),
        ('formation_annulee', 'Formation annulée'),
        ('formateur_ajoute', 'Formateur ajouté'),
        ('partenaire_ajoute', 'Partenaire ajouté'),
        ('partenaire_modifie', 'Partenaire modifié'),
        ('ressource_allouee', 'Ressource allouée'),
        ('planning_valide', 'Planning validé'),
        ('evenement_cree', 'Événement créé'),
        ('stock_modifie', 'Stock modifié'),
        # Qualité
        ('audit_lance', 'Audit lancé'),
        ('audit_termine', 'Audit terminé'),
        ('nc_signalée', 'Non-conformité signalée'),
        ('nc_traitee', 'Non-conformité traitée'),
        ('innovation_proposee', 'Innovation proposée'),
        ('innovation_validee', 'Innovation validée'),
        ('indicateur_cree', 'Indicateur créé'),
        ('indicateur_modifie', 'Indicateur modifié'),
        ('sondage_cree', 'Sondage créé'),
        ('amelioration_proposee', 'Amélioration proposée'),
        # Support
        ('ticket_cree', 'Ticket créé'),
        ('ticket_assigné', 'Ticket assigné'),
        ('ticket_resolu', 'Ticket résolu'),
        ('ticket_ferme', 'Ticket fermé'),
        ('chat_envoye', 'Chat envoyé'),
        ('message_repondu', 'Message répondu'),
        ('faq_maj', 'FAQ mise à jour'),
        ('utilisateur_ajoute', 'Utilisateur ajouté'),
        ('role_modifie', 'Rôle modifié'),
        ('compte_suspendu', 'Compte suspendu'),
        # Design
        ('maquette_cree', 'Maquette créée'),
        ('maquette_modifiee', 'Maquette modifiée'),
        ('maquette_validee', 'Maquette validée'),
        ('composant_cree', 'Composant UI créé'),
        ('composant_modifie', 'Composant UI modifié'),
        ('test_ux_lance', 'Test UX lancé'),
        ('test_ux_termine', 'Test UX terminé'),
        ('audit_ux', 'Audit UX réalisé'),
        ('design_system_maj', 'Design System mis à jour'),
        ('prototype_cree', 'Prototype créé'),
        # Direction Générale
        ('export_messages', 'Export messages'),
        ('export_candidatures', 'Export candidatures'),
        ('rapport_hebdo', 'Rapport hebdomadaire'),
        ('message_coordinateurs', 'Message aux coordinateurs'),
        ('archivage_messages', 'Archivage messages'),
        ('audit_departement', 'Audit département'),
        ('validation_budget', 'Validation budget'),
        ('alerte_cree', 'Alerte créée'),
        ('partenaire_dg', 'Partenaire ajouté (DG)'),
        ('cache_vide', 'Cache vidé'),
        # Finances & Abonnements
        ('paiement', 'Paiement'),
        ('paiement_confirme', 'Paiement confirmé'),
        ('paiement_echoue', 'Paiement échoué'),
        ('abonnement_active', 'Abonnement activé'),
        ('abonnement_expire', 'Abonnement expiré'),
        ('abonnement_renouvele', 'Abonnement renouvelé'),
        ('remboursement', 'Remboursement'),
        # Assistant IA
        ('chatbot', 'Question IA'),
        ('chatbot_bloque', 'Question IA bloquée'),
        ('chatbot_quota', 'Quota IA atteint'),
        # Sécurité & Système
        ('erreur', 'Erreur système'),
        ('acces_vault', 'Accès Vault'),
        ('configuration', 'Modification configuration'),
        ('sauvegarde_reussie', 'Sauvegarde réussie'),
        ('sauvegarde_echouee', 'Sauvegarde échouée'),
        ('haute_charge', 'Haute charge serveur'),
        # Support & Contact
        ('message_contact', 'Message de contact'),
        ('newsletter_inscription', 'Inscription newsletter'),
        # Recrutement
        ('candidature_envoyee', 'Candidature envoyée'),
        ('modification_statut', 'Modification statut candidature'),
        ('offre_publiee', 'Offre publiée'),
        # Communauté
        ('sujet_cree', 'Sujet forum créé'),
        ('message_forum', 'Message forum'),
        ('sujet_epingle', 'Sujet épinglé'),
        ('sujet_ferme', 'Sujet fermé'),
    ]

    GRAVITE_CHOICES = [
        ('info', 'Information'),
        ('avertissement', 'Avertissement'),
        ('critique', 'Critique'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='logs_audit'
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES, db_index=True)
    gravite = models.CharField(max_length=15, choices=GRAVITE_CHOICES, default='info')
    objet = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    donnees_json = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    hash_precedent = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Entrée d\'audit'
        verbose_name_plural = 'Journal d\'audit'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['action']),
            models.Index(fields=['gravite']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['utilisateur', 'timestamp']),
        ]

    def __str__(self):
        return f'[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.get_action_display()} - {self.objet}'

    def save(self, *args, **kwargs):
        if self.pk:
            raise PermissionError('Le journal d\'audit est immutable. Modification interdite.')
        
        # Chaîne de hachage
        dernier = AuditLog.objects.order_by('-timestamp').first()
        if dernier:
            chaine = f'{dernier.id}-{dernier.action}-{dernier.objet}-{dernier.timestamp.isoformat()}'
            self.hash_precedent = hashlib.sha256(chaine.encode()).hexdigest()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise PermissionError('Le journal d\'audit est immutable. Suppression interdite.')
