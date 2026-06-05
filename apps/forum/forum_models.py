"""
Forums communautaires.
Version corrigée et complète.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Forum(models.Model):
    METIER_CHOICES = [
        ('pilote_de_ligne', 'Pilote de ligne'),
        ('personnel_navigant', 'Personnel Navigant (PNC)'),
        ('ingenieur_aeronautique', 'Ingénieur Aéronautique'),
        ('controleur_aerien', 'Contrôleur Aérien'),
        ('technicien_aeronautique', 'Technicien Aéronautique'),
        ('mecanicien_avion', 'Mécanicien Avion'),
        ('agent_escale', 'Agent d\'Escale'),
        ('formation_avancee', 'Formation Avancée Premium'),
        ('general', 'Forum Général'),
    ]

    metier = models.CharField(max_length=30, choices=METIER_CHOICES, unique=True)
    nom = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, default='fa-comments')
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    gestionnaires = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='forums_geres',
        blank=True,
        limit_choices_to={'role__in': ['gestionnaire', 'coordinateur', 'dg']}
    )

    class Meta:
        verbose_name = 'Forum'
        verbose_name_plural = 'Forums'
        ordering = ['ordre']

    def __str__(self):
        return self.nom

    @property
    def total_sujets(self):
        return self.sujets.count()

    @property
    def total_messages(self):
        from django.db.models import Sum
        return self.sujets.aggregate(total=Sum('total_reponses'))['total'] or 0


class SousForum(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='sous_forums')
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='fa-folder')
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sous-forum'
        verbose_name_plural = 'Sous-forums'
        ordering = ['forum', 'ordre']
        unique_together = ['forum', 'slug']

    def __str__(self):
        return f'{self.forum.nom} > {self.nom}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Sujet(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='sujets')
    sous_forum = models.ForeignKey(SousForum, on_delete=models.SET_NULL, null=True, blank=True, related_name='sujets')
    titre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sujets_forum')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_message = models.DateTimeField(auto_now=True)
    total_reponses = models.IntegerField(default=0)
    total_vues = models.IntegerField(default=0)
    est_epingle = models.BooleanField(default=False)
    est_ferme = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Sujet'
        verbose_name_plural = 'Sujets'
        ordering = ['-est_epingle', '-date_dernier_message']
        indexes = [
            models.Index(fields=['forum', '-date_dernier_message']),
            models.Index(fields=['sous_forum', '-date_dernier_message']),
        ]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


class Message(models.Model):
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_forum')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_modere = models.BooleanField(default=False)
    modere_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages_moderes')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['date_creation']

    def __str__(self):
        return f'Message de {self.auteur.email} dans {self.sujet.titre}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Mettre à jour le compteur de réponses du sujet
            self.sujet.total_reponses = self.sujet.messages.count() - 1
            self.sujet.date_dernier_message = self.date_creation
            self.sujet.save(update_fields=['total_reponses', 'date_dernier_message'])
