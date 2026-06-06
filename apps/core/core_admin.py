from django.contrib import admin
from .models import SiteConfig, PageStatique, DocumentVault


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['nom', 'maintenance_mode']

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageStatique)
class PageStatiqueAdmin(admin.ModelAdmin):
    list_display = ['type_page', 'titre', 'version', 'approuve_par_dg', 'derniere_modification']
    list_filter = ['approuve_par_dg', 'archive']
    search_fields = ['titre', 'contenu']
    readonly_fields = ['derniere_modification', 'version']

    fieldsets = (
        ('Contenu', {'fields': ('type_page', 'titre', 'contenu')}),
        ('Approbation', {
            'fields': ('approuve_par_dg', 'approuve_par_coordinateurs'),
            'description': 'Manifeste §9.3 : Les pages légales doivent être approuvées par tous les coordinateurs et le DG.'
        }),
        ('Versionnage', {'fields': ('version', 'archive')}),
        ('Métadonnées', {'fields': ('modifie_par', 'derniere_modification')}),
    )

    def save_model(self, request, obj, form, change):
        obj.modifie_par = request.user
        if change:
            obj.version += 1
        super().save_model(request, obj, form, change)


@admin.register(DocumentVault)
class DocumentVaultAdmin(admin.ModelAdmin):
    list_display = ['nom', 'proprietaire', 'date_upload', 'taille']
    search_fields = ['nom', 'proprietaire__email']
    readonly_fields = ['date_upload']
