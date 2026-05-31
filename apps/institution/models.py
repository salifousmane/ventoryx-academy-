from django.db import models
from apps.users.models import User

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    parcours_name = models.CharField(max_length=200)
    certificate_hash = models.CharField(max_length=64, unique=True)  # SHA-256
    issued_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.parcours_name}"

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('under_review', 'En cours d\'examen'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    )
    
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_letter = models.TextField()
    resume_url = models.URLField()
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.candidate.username} - {self.job_posting.title}"