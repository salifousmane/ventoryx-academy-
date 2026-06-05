from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Subscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'departement', 'is_active')
    list_filter = ('role', 'departement', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'departement', 'telephone', 'date_naissance', 'photo', 'bio', 'langue_preference', 'abonnement_actif')
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'statut', 'date_debut', 'date_fin')
    list_filter = ('plan_type', 'statut')
