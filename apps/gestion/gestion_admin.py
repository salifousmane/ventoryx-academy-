from django.contrib import admin
from .models import Tache, Campagne, TicketSupport


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ['titre', 'departement', 'priorite', 'statut', 'progression', 'assigne_a', 'date_echeance']
    list_filter = ['departement', 'priorite', 'statut']
    search_fields = ['titre', 'description']
    readonly_fields = ['date_creation', 'date_modification']


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'departement', 'plateforme', 'statut', 'date_debut', 'date_fin']
    list_filter = ['departement', 'plateforme', 'statut']
    search_fields = ['nom', 'description']


@admin.register(TicketSupport)
class TicketSupportAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'utilisateur', 'priorite', 'statut', 'date_creation']
    list_filter = ['priorite', 'statut', 'departement']
    search_fields = ['sujet', 'description', 'utilisateur__email']
