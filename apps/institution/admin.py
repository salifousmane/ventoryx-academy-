from django.contrib import admin
from .models import OffreEmploi, Candidature, Certificat


@admin.register(OffreEmploi)
class OffreEmploiAdmin(admin.ModelAdmin):
    list_display = ('titre', 'departement', 'type_contrat', 'statut', 'date_publication')
    list_filter = ('statut',)
    search_fields = ('titre', 'description')


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'poste', 'statut', 'date_soumission')
    list_filter = ('statut',)
    search_fields = ('nom', 'prenom', 'email', 'poste')


@admin.register(Certificat)
class CertificatAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'full_name', 'parcours', 'statut', 'date_delivrance')
    list_filter = ('statut',)
    search_fields = ('numero_serie', 'full_name')
