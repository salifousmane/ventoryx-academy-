from django.contrib import admin
from .models import Parcours, ModuleParcours, CoursItem, ProgressionUtilisateur, Question, Reponse


class ModuleInline(admin.TabularInline):
    model = ModuleParcours
    extra = 0


@admin.register(Parcours)
class ParcoursAdmin(admin.ModelAdmin):
    list_display = ['nom', 'metier', 'gratuit', 'premium', 'actif', 'total_modules', 'total_cours']
    list_filter = ['gratuit', 'premium', 'actif']
    search_fields = ['nom']
    inlines = [ModuleInline]


@admin.register(ModuleParcours)
class ModuleParcoursAdmin(admin.ModelAdmin):
    list_display = ['parcours', 'numero', 'titre', 'cours_count', 'quiz_count', 'actif']
    list_filter = ['parcours', 'actif']


@admin.register(CoursItem)
class CoursItemAdmin(admin.ModelAdmin):
    list_display = ['module', 'type', 'numero', 'titre', 'actif']
    list_filter = ['type', 'actif', 'module__parcours']
    search_fields = ['titre']


class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 4
    max_num = 10
    fields = ['texte', 'est_correcte', 'position_correcte', 'ordre']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'type', 'ordre', 'texte_court']
    list_filter = ['type', 'test__module__parcours']
    search_fields = ['texte']
    inlines = [ReponseInline]
    fieldsets = (
        (None, {'fields': ('test', 'type', 'ordre')}),
        ('Contenu', {'fields': ('texte', 'reponse_texte', 'explication')}),
    )

    def texte_court(self, obj):
        return obj.texte[:80]
    texte_court.short_description = 'Question'


@admin.register(ProgressionUtilisateur)
class ProgressionUtilisateurAdmin(admin.ModelAdmin):
    list_display = ['user', 'parcours', 'termine', 'score', 'date_modification']
    list_filter = ['termine', 'parcours']
    search_fields = ['user__email']
