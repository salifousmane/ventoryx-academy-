from django.contrib import admin
from .models import MessageContact, Notification


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'categorie', 'statut', 'date_envoi')
    list_filter = ('categorie', 'statut')
    search_fields = ('nom', 'email', 'sujet')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'titre', 'type', 'lue', 'date_creation')
    list_filter = ('type', 'lue')
