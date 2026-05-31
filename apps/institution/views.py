from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Certificate, JobPosting, JobApplication

@require_http_methods(["GET"])
def careers(request):
    """View all career opportunities"""
    jobs = JobPosting.objects.filter(is_published=True)
    return render(request, 'pages/recrutement/carriere.html', {'jobs': jobs})

@require_http_methods(["GET"])
def verify_certificate(request):
    """Verify a certificate"""
    return render(request, 'pages/utilisateur/verification_certificat.html')