from django.contrib import admin
from .models import Candidature, OffreEmploi, Certificat
from django.utils import timezone


@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'poste', 'statut', 'date_soumission']
    list_filter = ['statut', 'poste']
    search_fields = ['nom', 'prenom', 'email']
    readonly_fields = ['date_soumission', 'date_modification']

    fieldsets = (
        ('Candidat', {'fields': ('nom', 'prenom', 'email', 'telephone')}),
        ('Candidature', {'fields': ('poste', 'message', 'cv', 'lettre_motivation')}),
        ('Traitement', {'fields': ('statut', 'traite_par', 'notes_internes')}),
        ('Dates', {'fields': ('date_soumission', 'date_modification')}),
    )
    
    def save_model(self, request, obj, form, change):
        if 'statut' in form.changed_data:
            from apps.audit.models import AuditLog
            AuditLog.objects.create(
                utilisateur=request.user,
                action='modification_statut',
                objet=f'Candidature {obj.nom} {obj.prenom} → {obj.get_statut_display()}',
                ip_address=request.META.get('REMOTE_ADDR', ''),
            )
        super().save_model(request, obj, form, change)


@admin.register(OffreEmploi)
class OffreEmploiAdmin(admin.ModelAdmin):
    list_display = ['titre', 'departement', 'statut', 'date_publication']
    list_filter = ['statut', 'departement', 'type_contrat']
    search_fields = ['titre', 'description']
    
    def save_model(self, request, obj, form, change):
        if obj.statut == 'publiee' and not obj.date_publication:
            obj.date_publication = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Certificat)
class CertificatAdmin(admin.ModelAdmin):
    list_display = ['numero_serie', 'full_name', 'parcours', 'statut', 'date_delivrance']
    list_filter = ['parcours', 'statut']
    search_fields = ['full_name', 'numero_serie', 'hash_verification']
    readonly_fields = ['hash_verification', 'date_delivrance']
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'role', '') == 'dg'
