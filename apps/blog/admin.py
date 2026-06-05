from django.contrib import admin
from .models import Article, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'statut', 'date_creation')
    list_filter = ('statut', 'categorie')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
