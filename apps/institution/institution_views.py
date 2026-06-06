"""Vues recrutement."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from .models import OffreEmploi, Candidature


def carriere(request):
    offres = OffreEmploi.objects.filter(statut='publiee').order_by('-date_publication')
    return render(request, 'pages/recrutement/carriere.html', {
        'page_title': 'Carrières',
        'offres': offres,
    })


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@csrf_protect
def postuler(request, offre_id=None):
    offre = None
    if offre_id:
        offre = get_object_or_404(OffreEmploi, id=offre_id, statut='publiee')

    if request.method == 'POST':
        # Honeypot anti-bot
        if request.POST.get('website'):
            messages.error(request, 'Erreur lors de l\'envoi.')
            return redirect('institution:carriere')
        
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        message = request.POST.get('message', '').strip()
        poste = request.POST.get('poste', offre.titre if offre else 'Candidature spontanée')

        if nom and prenom and email:
            Candidature.objects.create(
                poste=poste, nom=nom, prenom=prenom,
                email=email, telephone=telephone, message=message,
            )
            messages.success(request, 'Votre candidature a été envoyée avec succès.')
            return redirect('institution:carriere')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'pages/recrutement/postuler.html', {
        'page_title': 'Postuler',
        'offre': offre,
    })


@login_required
def espace_candidat(request):
    candidatures = Candidature.objects.filter(email=request.user.email).order_by('-date_soumission')
    return render(request, 'pages/recrutement/espace_candidat.html', {
        'page_title': 'Espace candidat',
        'candidatures': candidatures,
    })
