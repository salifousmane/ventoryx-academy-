from django.shortcuts import render
from .models import Candidature, OffreEmploi, Certificat


def index(request):
    return render(request, 'pages/institution/a_propos.html', {'page_title': 'Institution'})
