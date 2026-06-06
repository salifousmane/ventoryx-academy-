"""
Modèles : parcours, modules, cours, tests, progression, questions.
"""
from django.db import models
from django.conf import settings


class Parcours(models.Model):
    METIER_CHOICES = [
        ('pilote_de_ligne', 'Pilote de ligne'),
        ('personnel_navigant', 'Personnel Navigant (PNC)'),
        ('ingenieur_aeronautique', 'Ingénieur Aéronautique'),
        ('controleur_aerien', 'Contrôleur Aérien'),
        ('technicien_aeronautique', 'Technicien Aéronautique'),
        ('mecanicien_avion', 'Mécanicien Avion'),
        ('agent_escale', 'Agent d\'Escale'),
        ('formation_avancee', 'Formation Avancée Premium'),
    ]

    metier = models.CharField(max_length=50, choices=METIER_CHOICES, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='fa-plane')
    gratuit = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Parcours'
        verbose_name_plural = 'Parcours'
        ordering = ['ordre']

    def __str__(self):
        return self.nom

    @property
    def total_modules(self):
        return self.modules.count()

    @property
    def total_cours(self):
        return self.modules.aggregate(total=models.Sum('cours_count'))['total'] or 0

    @property
    def total_quiz(self):
        return self.modules.aggregate(total=models.Sum('quiz_count'))['total'] or 0


class ModuleParcours(models.Model):
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE, related_name='modules')
    numero = models.IntegerField()
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cours_count = models.IntegerField(default=20)
    quiz_count = models.IntegerField(default=4)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ['parcours', 'numero']
        unique_together = ['parcours', 'numero']

    def __str__(self):
        return f'{self.parcours.nom} — Module {self.numero} : {self.titre}'


class CoursItem(models.Model):
    TYPE_CHOICES = [
        ('cours', 'Cours'),
        ('quiz', 'Quiz'),
        ('test', 'Test'),
    ]

    module = models.ForeignKey(ModuleParcours, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='cours')
    numero = models.IntegerField()
    titre = models.CharField(max_length=200)
    contenu = models.TextField(blank=True)
    duree_estimee = models.IntegerField(default=30)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cours/Quiz'
        verbose_name_plural = 'Cours/Quiz'
        ordering = ['module', 'numero']
        unique_together = ['module', 'numero']

    def __str__(self):
        return f'{self.module} — {self.get_type_display()} {self.numero} : {self.titre}'


class Question(models.Model):
    TYPE_CHOICES = [
        ('qcm_simple', 'QCM — Une seule réponse'),
        ('qcm_multiple', 'QCM — Plusieurs réponses'),
        ('vrai_faux', 'Vrai ou Faux'),
        ('texte_trous', 'Texte à trous'),
        ('reorganisation', 'Remise en ordre'),
    ]

    test = models.ForeignKey(
        CoursItem, on_delete=models.CASCADE,
        related_name='questions',
        limit_choices_to={'type': 'test'}
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='qcm_simple')
    texte = models.TextField(help_text='Consigne ou question')
    reponse_texte = models.CharField(max_length=500, blank=True,
        help_text='Réponse attendue pour les textes à trous')
    explication = models.TextField(blank=True,
        help_text='Explication affichée après correction')
    ordre = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['ordre']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.texte[:60]}'


class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.TextField()
    est_correcte = models.BooleanField(default=False)
    ordre = models.IntegerField(default=0)
    position_correcte = models.IntegerField(null=True, blank=True,
        help_text='Position correcte pour la remise en ordre (1, 2, 3...)')

    class Meta:
        verbose_name = 'Réponse'
        verbose_name_plural = 'Réponses'
        ordering = ['ordre']

    def __str__(self):
        prefix = '✅' if self.est_correcte else '❌'
        return f'{prefix} {self.texte[:50]}'


class ProgressionUtilisateur(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progressions')
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleParcours, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(CoursItem, on_delete=models.SET_NULL, null=True, blank=True)
    termine = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    tentatives = models.IntegerField(default=0)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Progression utilisateur'
        verbose_name_plural = 'Progressions utilisateurs'
        ordering = ['-date_modification']

    def __str__(self):
        return f'{self.user.email} — {self.parcours.nom}'
