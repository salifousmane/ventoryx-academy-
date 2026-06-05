from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Catégorie'
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Article(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]

    titre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    contenu = models.TextField()
    resume = models.TextField(blank=True)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='articles',
    )
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    vues = models.IntegerField(default=0)
    meta_description = models.CharField(max_length=300, blank=True)
    mots_cles = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Article'
        ordering = ['-date_creation']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
