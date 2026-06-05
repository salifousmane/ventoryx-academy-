from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'action', 'gravite', 'objet', 'utilisateur', 'ip_address', 'hash_precedent']
    list_filter = ['action', 'gravite', 'timestamp']
    search_fields = ['objet', 'description', 'utilisateur__email']
    readonly_fields = ['utilisateur', 'action', 'gravite', 'objet', 'description',
                       'ip_address', 'user_agent', 'donnees_json', 'timestamp', 'hash_precedent']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
