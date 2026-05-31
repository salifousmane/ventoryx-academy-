from django.db import models
from apps.users.models import User

class Parcours(models.Model):
    METIER_CHOICES = (
        ('pnc', 'PNC'),
        ('pilote', 'Pilote de Ligne'),
        ('ingenieur', 'Ingénieur Aéronautique'),
        ('controleur', 'Contrôleur Aérien'),
        ('technicien', 'Technicien Aéronautique'),
        ('mecanicien', 'Mécanicien Avion'),
        ('agent', 'Agent d\'Escale'),
        ('premium', 'Formation Avancée (Premium)'),
    )
    
    name = models.CharField(max_length=200)
    metier = models.CharField(max_length=20, choices=METIER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    modules_count = models.IntegerField(default=0)
    courses_count = models.IntegerField(default=0)
    tests_count = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Module(models.Model):
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.parcours.name} - {self.title}"

class Course(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    content = models.TextField()
    duration = models.IntegerField()  # in minutes
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.parcours.name} - {self.title}"

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    passing_score = models.IntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"