from django.contrib import admin
from apps.core.models import SiteConfig, PageStatique, DocumentVault


@admin.register(PageStatique)
class PageStatiqueAdmin(admin.ModelAdmin):
    list_display = ('type_page', 'approuve_par_dg', 'archive')
    list_filter = ('type_page', 'approuve_par_dg', 'archive')
    search_fields = ('type_page', 'contenu')
    ordering = ('-derniere_modification',)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(DocumentVault)
class DocumentVaultAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_document', 'date_upload')
