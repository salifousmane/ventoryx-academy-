from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('dg', 'DG'),
        ('coordinateur', 'Coordinateur'),
        ('gestionnaire', 'Gestionnaire'),
    )
    
    DEPT_CHOICES = (
        ('pedagogie', 'Pédagogie'),
        ('technique', 'Technique'),
        ('marketing', 'Marketing'),
        ('operations', 'Opérations'),
        ('qualite', 'Qualité'),
        ('support', 'Support'),
        ('design', 'Design'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='gestionnaire')
    department = models.CharField(max_length=20, choices=DEPT_CHOICES, null=True, blank=True)
    is_active_account = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"