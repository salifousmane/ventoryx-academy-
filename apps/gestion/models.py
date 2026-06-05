from django.db import models
from django.conf import settings


class Tache(models.Model):
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('critique', 'Critique'),
    ]

    STATUT_CHOICES = [
        ('a_faire', 'À faire'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    DEPARTEMENT_CHOICES = [
        ('pedagogie', 'Pédagogie'),
        ('technique', 'Technique'),
        ('marketing', 'Marketing'),
        ('operations', 'Opérations'),
        ('qualite', 'Qualité'),
        ('support', 'Support'),
        ('design', 'Design'),
    ]

    titre = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    departement = models.CharField(max_length=20, choices=DEPARTEMENT_CHOICES)
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='normale')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='a_faire')
    assigne_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='taches_assignees',
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_echeance = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Tâche'
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre


class Campagne(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('planifiee', 'Planifiée'),
        ('active', 'Active'),
        ('terminee', 'Terminée'),
    ]

    PLATEFORME_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('reseaux_sociaux', 'Réseaux sociaux'),
        ('push', 'Push notification'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    plateforme = models.CharField(max_length=20, choices=PLATEFORME_CHOICES, default='email')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='brouillon')
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='campagnes_creees',
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Campagne'
        ordering = ['-date_creation']

    def __str__(self):
        return self.nom


class TicketSupport(models.Model):
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
        ('critique', 'Critique'),
    ]

    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]

    sujet = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ouvert')
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_support',
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ticket support'
        ordering = ['-date_creation']

    def __str__(self):
        return self.sujet
