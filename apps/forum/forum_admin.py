from django.contrib import admin
from .models import Forum, SousForum, Sujet, Message


class SousForumInline(admin.TabularInline):
    model = SousForum
    extra = 1
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['nom', 'metier', 'ordre', 'actif', 'sujets_count', 'messages_count']
    list_filter = ['actif', 'metier']
    search_fields = ['nom', 'description']
    inlines = [SousForumInline]
    filter_horizontal = ['gestionnaires']
    
    def sujets_count(self, obj):
        return obj.sujets.count()
    sujets_count.short_description = 'Sujets'
    
    def messages_count(self, obj):
        return sum(s.total_reponses + 1 for s in obj.sujets.all())
    messages_count.short_description = 'Messages'


@admin.register(SousForum)
class SousForumAdmin(admin.ModelAdmin):
    list_display = ['nom', 'forum', 'ordre', 'actif']
    list_filter = ['forum', 'actif']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'forum', 'auteur', 'date_creation', 'total_reponses', 'est_epingle', 'est_ferme']
    list_filter = ['forum', 'est_epingle', 'est_ferme']
    search_fields = ['titre', 'contenu', 'auteur__email']
    readonly_fields = ['date_creation', 'date_dernier_message', 'total_vues', 'total_reponses']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'auteur', 'date_creation', 'date_modification']
    list_filter = ['date_creation']
    search_fields = ['contenu', 'auteur__email']
    readonly_fields = ['date_creation', 'date_modification']
