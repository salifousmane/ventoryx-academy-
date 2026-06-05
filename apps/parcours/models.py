from django.db import models
from django.conf import settings


class Parcours(models.Model):
    METIER_CHOICES = [
        ('pilote_de_ligne', 'Pilote de ligne'),
        ('personnel_navigant', 'Personnel Navigant Commercial'),
        ('ingenieur_aeronautique', 'Ingénieur aéronautique'),
        ('controleur_aerien', 'Contrôleur aérien'),
        ('technicien_aeronautique', 'Technicien aéronautique'),
        ('mecanicien_avion', 'Mécanicien avion'),
        ('agent_escale', "Agent d'escale"),
        ('formation_avancee', 'Formation avancée'),
    ]

    nom = models.CharField(max_length=200)
    metier = models.CharField(max_length=50, choices=METIER_CHOICES, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='parcours/', null=True, blank=True)
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    gratuit = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    duree_estimee = models.IntegerField(default=0, help_text='Durée en heures')

    class Meta:
        verbose_name = 'Parcours'
        verbose_name_plural = 'Parcours'
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    @property
    def total_cours(self):
        return CoursItem.objects.filter(module__parcours=self, type='cours', actif=True).count()

    @property
    def total_quiz(self):
        return CoursItem.objects.filter(module__parcours=self, type='test', actif=True).count()


class ModuleParcours(models.Model):
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE, related_name='modules')
    numero = models.IntegerField()
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Module'
        unique_together = ('parcours', 'numero')
        ordering = ['numero']

    def __str__(self):
        return f"{self.parcours.nom} — Module {self.numero}: {self.titre}"


class CoursItem(models.Model):
    TYPE_CHOICES = [
        ('cours', 'Cours'),
        ('test', 'Test'),
    ]

    module = models.ForeignKey(ModuleParcours, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    numero = models.IntegerField()
    titre = models.CharField(max_length=200)
    contenu = models.TextField(blank=True)
    duree_estimee = models.IntegerField(default=30, help_text='Durée en minutes')
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cours/Test'
        unique_together = ('module', 'type', 'numero')
        ordering = ['numero']

    def __str__(self):
        return f"{self.module} — {self.get_type_display()} {self.numero}: {self.titre}"


class Question(models.Model):
    TYPE_CHOICES = [
        ('qcm_simple', 'QCM simple'),
        ('qcm_multiple', 'QCM multiple'),
        ('vrai_faux', 'Vrai/Faux'),
        ('texte_trous', 'Texte à trous'),
        ('reorganisation', 'Réorganisation'),
    ]

    test = models.ForeignKey(CoursItem, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='qcm_simple')
    texte = models.TextField()
    reponse_texte = models.CharField(max_length=500, blank=True)
    explication = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        ordering = ['ordre']

    def __str__(self):
        return f"{self.test.titre} — Q{self.ordre}: {self.texte[:50]}"


class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=500)
    est_correcte = models.BooleanField(default=False)
    position_correcte = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Réponse'
        ordering = ['position_correcte']

    def __str__(self):
        return f"{self.question} — {self.texte[:50]}"


class ProgressionUtilisateur(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progressions')
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleParcours, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(CoursItem, on_delete=models.CASCADE, null=True, blank=True)
    termine = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    tentatives = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Progression utilisateur'
        unique_together = ('user', 'parcours', 'module', 'item')

    def __str__(self):
        return f"{self.user} — {self.parcours.nom}"
