from django.contrib import admin
from .models import Tache, Campagne, TicketSupport


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'departement', 'priorite', 'statut', 'date_creation')
    list_filter = ('departement', 'priorite', 'statut')


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'plateforme', 'statut', 'date_creation')
    list_filter = ('plateforme', 'statut')


@admin.register(TicketSupport)
class TicketSupportAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'priorite', 'statut', 'utilisateur', 'date_creation')
    list_filter = ('priorite', 'statut')
