from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('gestionnaire', 'Gestionnaire'),
        ('coordinateur', 'Coordinateur'),
        ('dg', 'Directeur Général'),
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

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')
    departement = models.CharField(max_length=20, choices=DEPARTEMENT_CHOICES, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    otp_secret = models.CharField(max_length=32, blank=True)
    otp_enabled = models.BooleanField(default=False)
    langue_preference = models.CharField(max_length=5, default='fr')
    abonnement_actif = models.BooleanField(default=False)
    rgpd_consent = models.BooleanField(default=False)
    date_rgpd_consent = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def is_dg(self):
        return self.role == 'dg'

    @property
    def is_coordinateur(self):
        return self.role == 'coordinateur'

    @property
    def is_gestionnaire(self):
        return self.role == 'gestionnaire'

    @property
    def is_etudiant(self):
        return self.role == 'etudiant'


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel'),
        ('bienvenue_annuel', 'Bienvenue Annuel'),
        ('entreprise', 'Entreprise'),
    ]

    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Annulée'),
        ('past_due', 'En retard'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='mensuel')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='inactive')
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Abonnement'

    def __str__(self):
        return f"{self.user} — {self.plan_type}"

    def est_active(self):
        from django.utils import timezone
        if self.statut != 'active':
            return False
        if self.date_fin and self.date_fin < timezone.now():
            return False
        return True
