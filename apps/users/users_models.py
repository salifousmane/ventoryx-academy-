"""
Modèles utilisateurs, abonnements.
Manifeste §1.3 : OAuth Google + fallback email.
Manifeste §3.2 : RBAC 3 niveaux (DG > Coordinateur > Gestionnaire).
Manifeste §7 : Abonnement avec offre de bienvenue (3 premiers).
Manifeste §4.1 : Nationalité et date de naissance obligatoires.
Manifeste §A : OTP pour actions critiques DG.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email obligatoire.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_dg', True)
        extra_fields.setdefault('role', 'dg')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('dg', 'Directeur Général'),
        ('coordinateur', 'Coordinateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('candidat', 'Candidat'),
        ('etudiant', 'Étudiant'),
    ]

    NATIONALITE_CHOICES = [
        ('FR', 'Française'), ('BE', 'Belge'), ('CH', 'Suisse'),
        ('CA', 'Canadienne'), ('MA', 'Marocaine'), ('DZ', 'Algérienne'),
        ('TN', 'Tunisienne'), ('SN', 'Sénégalaise'), ('CI', 'Ivoirienne'),
        ('CM', 'Camerounaise'), ('OTHER', 'Autre'),
    ]

    email = models.EmailField(unique=True)
    nationality = models.CharField(max_length=100, default='FR')
    date_naissance = models.DateField(null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidat')
    departement = models.CharField(max_length=30, blank=True, null=True)

    is_dg = models.BooleanField(default=False)
    is_coordinateur = models.BooleanField(default=False)
    is_gestionnaire = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_welcome_tier_1 = models.BooleanField(default=False)
    is_welcome_tier_2 = models.BooleanField(default=False)

    otp_secret = models.CharField(max_length=64, blank=True, null=True)
    otp_required = models.BooleanField(default=False)

    compte_google_id = models.CharField(max_length=255, blank=True, null=True)
    accepte_cookies_securite = models.BooleanField(default=False)

    date_inscription = models.DateTimeField(auto_now_add=True)
    email_notifications = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nationality', 'date_naissance']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_inscription']

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    @property
    def est_majeur(self):
        if not self.date_naissance:
            return False
        from django.conf import settings
        age_min = getattr(settings, 'AGE_MINIMUM', 16)
        today = timezone.now().date()
        age = today.year - self.date_naissance.year
        if today.month < self.date_naissance.month or (
            today.month == self.date_naissance.month and today.day < self.date_naissance.day
        ):
            age -= 1
        return age >= age_min

    @property
    def abonnement_actif(self):
        if self.is_dg or self.is_coordinateur or self.is_gestionnaire:
            return True
        if self.is_welcome_tier_1 or self.is_welcome_tier_2:
            return True
        try:
            return self.subscription.est_active()
        except Subscription.DoesNotExist:
            return False


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel'),
        ('bienvenue_mensuel', 'Bienvenue Mensuel (30 jours)'),
        ('bienvenue_annuel', 'Bienvenue Annuel (365 jours)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(max_length=30, choices=PLAN_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_auto_granted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    renouvelement_auto = models.BooleanField(default=True)
    date_dernier_paiement = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Abonnement'
        verbose_name_plural = 'Abonnements'

    def est_active(self):
        return self.is_active and self.end_date > timezone.now()

    def __str__(self):
        return f'{self.user.email} - {self.get_plan_type_display()}'


class ValidationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    action = models.CharField(max_length=100)
    cree_le = models.DateTimeField(auto_now_add=True)
    expire_le = models.DateTimeField()
    utilise = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Code de validation'
        verbose_name_plural = 'Codes de validation'

    def est_valide(self):
        return not self.utilise and self.expire_le > timezone.now()

    def __str__(self):
        return f'Code {self.code} - {self.action}'
