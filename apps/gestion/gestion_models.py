"""
Modèles de gestion pour les départements.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Tache(models.Model):
    """Tâche assignée à un département."""
    PRIORITE_CHOICES = [
        ('normale', 'Normale'),
        ('haute', 'Haute'),
        ('critique', 'Critique'),
    ]
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
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

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    departement = models.CharField(max_length=30, choices=DEPARTEMENT_CHOICES)
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='normale')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_cours')
    assigne_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    progression = models.IntegerField(default=0, help_text="Progression en pourcentage (0-100)")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_echeance = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Tâche'
        verbose_name_plural = 'Tâches'
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre


class Campagne(models.Model):
    """Campagne marketing."""
    PLATEFORME_CHOICES = [
        ('email', 'Email'),
        ('linkedin', 'LinkedIn'),
        ('google', 'Google Ads'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('active', 'Active'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    departement = models.CharField(max_length=30, default='marketing')
    plateforme = models.CharField(max_length=20, choices=PLATEFORME_CHOICES, default='email')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Campagne'
        verbose_name_plural = 'Campagnes'
        ordering = ['-date_creation']

    def __str__(self):
        return self.nom


class TicketSupport(models.Model):
    """Ticket de support."""
    PRIORITE_CHOICES = [
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
        ('urgent', 'Urgent'),
    ]
    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
    ]

    sujet = models.CharField(max_length=200)
    description = models.TextField()
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    departement = models.CharField(max_length=30, default='support')
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouvert')
    assigne_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assignes')
    reponse = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_resolution = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ticket support'
        verbose_name_plural = 'Tickets support'
        ordering = ['-date_creation']

    def __str__(self):
        return f'#{self.id} - {self.sujet}'
