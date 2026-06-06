"""
Modèles institutionnels.
Manifeste §3.2 : Candidatures, offres d'emploi, certificats.
Manifeste §5.2 : Certificats avec hash unique de vérification.
Manifeste §7.4 : Traçabilité dans le journal d'audit.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import hashlib
import uuid


class Candidature(models.Model):
    STATUT_CHOICES = [
        ('recue', 'Reçue'),
        ('en_revision', 'En révision'),
        ('entretien', 'Entretien proposé'),
        ('retenue', 'Candidat retenu'),
        ('refusee', 'Refusée'),
        ('archivee', 'Archivée'),
    ]

    poste = models.CharField(max_length=200)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=30, blank=True)
    message = models.TextField(blank=True)
    cv = models.FileField(upload_to='candidatures/cv/%Y/%m/', blank=True, null=True)
    lettre_motivation = models.FileField(upload_to='candidatures/lm/%Y/%m/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='recue', db_index=True)
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='candidatures_traitees'
    )
    notes_internes = models.TextField(blank=True)
    source = models.CharField(max_length=50, blank=True, help_text="Source de la candidature")

    class Meta:
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        ordering = ['-date_soumission']
        indexes = [
            models.Index(fields=['statut', '-date_soumission']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.prenom} {self.nom} - {self.poste}'


class OffreEmploi(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publiee', 'Publiée'),
        ('pourvue', 'Pourvue'),
        ('fermee', 'Fermée'),
    ]

    DEPARTEMENT_CHOICES = [
        ('pedagogie', 'Pédagogie & Contenu'),
        ('technique', 'Développement & Technique'),
        ('marketing', 'Marketing & Communication'),
        ('operations', 'Opérations & Logistique'),
        ('qualite', 'Qualité & Innovation'),
        ('support', 'Support & Administration'),
        ('design', 'Design & Expérience Utilisateur'),
    ]
    
    TYPE_CONTRAT_CHOICES = [
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('stage', 'Stage'),
        ('alternance', 'Alternance'),
        ('freelance', 'Freelance'),
        ('volontaire', 'Volontaire'),
    ]

    titre = models.CharField(max_length=200)
    departement = models.CharField(max_length=30, choices=DEPARTEMENT_CHOICES)
    description = models.TextField()
    competences = models.TextField(blank=True, help_text="Compétences requises")
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES, default='cdi')
    localisation = models.CharField(max_length=100, blank=True, help_text="Télétravail possible")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', db_index=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    date_expiration = models.DateTimeField(null=True, blank=True)
    salaire = models.CharField(max_length=100, blank=True, help_text="Ex: 35k-45k €/an")

    class Meta:
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"
        ordering = ['-date_publication', '-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.get_departement_display()}"


class Certificat(models.Model):
    """
    Certificat délivré après réussite du test global.
    Manifeste §5.2 : Signature numérique, hash unique inviolable.
    """
    STATUT_CHOICES = [
        ('valide', 'Valide'),
        ('revoke', 'Révoqué'),
        ('expire', 'Expiré'),
    ]

    numero_serie = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=200)
    parcours = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certificats'
    )
    date_delivrance = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='valide', db_index=True)
    hash_verification = models.CharField(max_length=64, unique=True, blank=True)
    score = models.IntegerField(default=0, help_text="Score obtenu au test global")
    pdf_file = models.FileField(upload_to='certificats/', blank=True, null=True)

    class Meta:
        verbose_name = 'Certificat'
        verbose_name_plural = 'Certificats'
        ordering = ['-date_delivrance']
        indexes = [
            models.Index(fields=['numero_serie']),
            models.Index(fields=['hash_verification']),
        ]

    def __str__(self):
        return f'{self.full_name} - {self.parcours} ({self.numero_serie})'

    def save(self, *args, **kwargs):
        if not self.numero_serie:
            self.numero_serie = f'VTX-{timezone.now().strftime("%Y%m%d")}-{uuid.uuid4().hex[:8].upper()}'
        if not self.hash_verification:
            chaine = f'{self.numero_serie}-{self.full_name}-{self.date_delivrance.isoformat()}-{self.score}'
            self.hash_verification = hashlib.sha256(chaine.encode()).hexdigest()
        super().save(*args, **kwargs)
