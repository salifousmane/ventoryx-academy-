from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'utilisateur', 'action', 'gravite', 'ip_address')
    list_filter = ('action', 'gravite')
    search_fields = ('utilisateur__email', 'objet', 'description')
    readonly_fields = ('timestamp',)
