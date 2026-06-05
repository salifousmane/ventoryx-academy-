from django.contrib import admin
from .models import Parcours, ModuleParcours, CoursItem, Question, Reponse, ProgressionUtilisateur


@admin.register(Parcours)
class ParcoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'metier', 'actif', 'gratuit', 'premium', 'ordre')
    list_filter = ('actif', 'gratuit', 'premium')


@admin.register(ModuleParcours)
class ModuleParcoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'parcours', 'numero', 'actif')
    list_filter = ('parcours', 'actif')


@admin.register(CoursItem)
class CoursItemAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'type', 'numero', 'actif')
    list_filter = ('type', 'actif')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('texte', 'test', 'type', 'ordre')
    list_filter = ('type',)


@admin.register(Reponse)
class ReponseAdmin(admin.ModelAdmin):
    list_display = ('texte', 'question', 'est_correcte')
    list_filter = ('est_correcte',)


@admin.register(ProgressionUtilisateur)
class ProgressionAdmin(admin.ModelAdmin):
    list_display = ('user', 'parcours', 'termine', 'score')
    list_filter = ('termine',)
