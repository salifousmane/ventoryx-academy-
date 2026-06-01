"""
Configuration globale du site.
"""
from django.db import models
from django.conf import settings


class SiteConfig(models.Model):
    nom = models.CharField(max_length=100, default='Ventoryx Academy')
    logo = models.ImageField(upload_to='config/', blank=True, null=True)
    favicon = models.ImageField(upload_to='config/', blank=True, null=True)
    couleur_primaire = models.CharField(max_length=7, default='#0F1C2E')
    couleur_secondaire = models.CharField(max_length=7, default='#0077B6')
    couleur_accent = models.CharField(max_length=7, default='#FF6B35')
    maintenance_mode = models.BooleanField(default=False)
    description_site = models.TextField(blank=True)
    mots_cles = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Configuration du site'
        verbose_name_plural = 'Configuration du site'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise PermissionError("La configuration ne peut pas être supprimée")

    def __str__(self):
        return self.nom


class PageStatique(models.Model):
    TYPE_CHOICES = [
        ('a_propos', 'À propos'),
        ('mentions_legales', 'Mentions légales'),
        ('cgu', 'Conditions Générales d\'Utilisation'),
        ('confidentialite', 'Politique de confidentialité'),
        ('cookies', 'Politique de cookies'),
        ('accessibilite', 'Accessibilité'),
    ]

    type_page = models.CharField(max_length=30, choices=TYPE_CHOICES, unique=True)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    derniere_modification = models.DateTimeField(auto_now=True)
    modifie_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    approuve_par_dg = models.BooleanField(default=False)
    approuve_par_coordinateurs = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    archive = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Page statique'
        verbose_name_plural = 'Pages statiques'
        ordering = ['type_page']

    def __str__(self):
        return self.get_type_page_display()
    
    def est_publicable(self):
        return self.approuve_par_dg and self.approuve_par_coordinateurs and not self.archive


class DocumentVault(models.Model):
    TYPE_CHOICES = [
        ('contrat', 'Contrat'),
        ('facture', 'Facture'),
        ('rapport', 'Rapport'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=255)
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    fichier = models.FileField(upload_to='vault/%Y/%m/')
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents_vault')
    description = models.TextField(blank=True)
    date_upload = models.DateTimeField(auto_now_add=True)
    taille = models.IntegerField(default=0)
    est_confidentiel = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Document (Vault)'
        verbose_name_plural = 'Documents (Vault)'
        ordering = ['-date_upload']

    def save(self, *args, **kwargs):
        if self.fichier:
            self.taille = self.fichier.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
