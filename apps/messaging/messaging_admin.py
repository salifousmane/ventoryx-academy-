from django.contrib import admin
from .models import MessageContact, Notification, NewsletterInscription


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'nom', 'email', 'categorie', 'statut', 'date_envoi']
    list_filter = ['statut', 'categorie']
    search_fields = ['nom', 'email', 'sujet', 'message']
    readonly_fields = ['date_envoi', 'date_reponse']
    
    fieldsets = (
        ('Expéditeur', {'fields': ('nom', 'email')}),
        ('Message', {'fields': ('sujet', 'message', 'categorie')}),
        ('Traitement', {'fields': ('statut', 'traite_par', 'reponse', 'date_reponse')}),
        ('Dates', {'fields': ('date_envoi',)}),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'destinataire', 'type', 'est_lue', 'date_creation']
    list_filter = ['type', 'est_lue']
    search_fields = ['titre', 'message', 'destinataire__email']
    readonly_fields = ['date_creation', 'date_lecture']


@admin.register(NewsletterInscription)
class NewsletterInscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'source', 'date_inscription', 'est_active']
    list_filter = ['est_active', 'source']
    search_fields = ['email']
