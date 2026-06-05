from django.contrib import admin
from .models import Forum, SousForum, Sujet, Message


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('nom', 'metier', 'actif', 'ordre')
    list_filter = ('actif',)


@admin.register(SousForum)
class SousForumAdmin(admin.ModelAdmin):
    list_display = ('nom', 'forum', 'actif')


@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'forum', 'auteur', 'date_creation', 'est_epingle', 'est_ferme')
    list_filter = ('est_epingle', 'est_ferme')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'auteur', 'date_creation')
