from django.db import models
from django.conf import settings


class OffreEmploi(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publiee', 'Publiée'),
        ('archivee', 'Archivée'),
    ]

    titre = models.CharField(max_length=300)
    description = models.TextField()
    departement = models.CharField(max_length=100, blank=True)
    localisation = models.CharField(max_length=200, blank=True)
    type_contrat = models.CharField(max_length=50, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')
    date_publication = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    STATUT_CHOICES = [
        ('soumise', 'Soumise'),
        ('en_cours', 'En cours d\'examen'),
        ('retenue', 'Retenue'),
        ('rejetee', 'Rejetée'),
    ]

    poste = models.CharField(max_length=300)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    cv = models.FileField(upload_to='candidatures/cv/', null=True, blank=True)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='soumise')
    date_soumission = models.DateTimeField(auto_now_add=True)
    notes_recruteur = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Candidature'
        ordering = ['-date_soumission']

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.poste}"


class Certificat(models.Model):
    STATUT_CHOICES = [
        ('valide', 'Valide'),
        ('revoke', 'Révoqué'),
    ]

    numero_serie = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=200)
    parcours = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificats',
    )
    hash_verification = models.CharField(max_length=64, unique=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='valide')
    date_delivrance = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Certificat'
        ordering = ['-date_delivrance']

    def __str__(self):
        return f"{self.numero_serie} — {self.full_name}"
