from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Forum(models.Model):
    METIER_CHOICES = [
        ('pilote_de_ligne', 'Pilote de ligne'),
        ('personnel_navigant', 'Personnel Navigant Commercial'),
        ('ingenieur_aeronautique', 'Ingénieur aéronautique'),
        ('controleur_aerien', 'Contrôleur aérien'),
        ('technicien_aeronautique', 'Technicien aéronautique'),
        ('mecanicien_avion', 'Mécanicien avion'),
        ('agent_escale', "Agent d'escale"),
        ('formation_avancee', 'Formation avancée'),
        ('general', 'Général'),
    ]

    nom = models.CharField(max_length=200)
    metier = models.CharField(max_length=50, choices=METIER_CHOICES, unique=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Forum'
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    @property
    def sujets(self):
        return Sujet.objects.filter(forum=self)


class SousForum(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='sous_forums')
    nom = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Sous-forum'
        ordering = ['ordre', 'nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.forum.nom} > {self.nom}"

    @property
    def sujets(self):
        return Sujet.objects.filter(sous_forum=self)


class Sujet(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='sujets_forum')
    sous_forum = models.ForeignKey(SousForum, on_delete=models.SET_NULL, null=True, blank=True, related_name='sujets_sous_forum')
    titre = models.CharField(max_length=300)
    contenu = models.TextField()
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sujets_forum')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_message = models.DateTimeField(auto_now=True)
    est_epingle = models.BooleanField(default=False)
    est_ferme = models.BooleanField(default=False)
    total_vues = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Sujet'
        ordering = ['-est_epingle', '-date_dernier_message']

    def __str__(self):
        return self.titre

    @property
    def total_reponses(self):
        return self.messages.count()


class Message(models.Model):
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_forum')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Message'
        ordering = ['date_creation']

    def __str__(self):
        return f"Message de {self.auteur} sur {self.sujet}"
