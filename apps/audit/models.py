from django.db import models
from apps.users.models import User
import hashlib

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('create', 'Création'),
        ('update', 'Mise à jour'),
        ('delete', 'Suppression'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('file_access', 'Accès fichier'),
        ('file_download', 'Téléchargement fichier'),
        ('file_upload', 'Téléversement fichier'),
        ('payment', 'Paiement'),
        ('refund', 'Remboursement'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100)
    resource_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    previous_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    previous_hash = models.CharField(max_length=64, null=True, blank=True)
    hash_value = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]
    
    def save(self, *args, **kwargs):
        # Generate hash for immutable chain
        hash_input = f"{self.previous_hash or ''}{self.user_id}{self.action}{self.resource_type}{self.created_at}"
        self.hash_value = hashlib.sha256(hash_input.encode()).hexdigest()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.action} - {self.resource_type}"