from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscription, ValidationCode


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'departement', 'is_active', 'date_inscription']
    list_filter = ['role', 'departement', 'is_active', 'is_dg', 'is_coordinateur', 'is_gestionnaire']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_inscription']

    fieldsets = (
        ('Identité', {'fields': ('email', 'first_name', 'last_name', 'nationality', 'date_naissance')}),
        ('Rôle', {'fields': ('role', 'departement', 'is_dg', 'is_coordinateur', 'is_gestionnaire', 'is_active', 'is_staff', 'is_superuser')}),
        ('Offre bienvenue', {'fields': ('is_welcome_tier_1', 'is_welcome_tier_2')}),
        ('Sécurité', {'fields': ('otp_required', 'otp_secret')}),
        ('Dates', {'fields': ('date_joined', 'last_login', 'date_inscription')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'nationality', 'date_naissance', 'password1', 'password2'),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan_type', 'start_date', 'end_date', 'est_active', 'is_auto_granted']
    list_filter = ['plan_type', 'is_auto_granted', 'is_active']
    search_fields = ['user__email']


@admin.register(ValidationCode)
class ValidationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'action', 'cree_le', 'expire_le', 'utilise']
    list_filter = ['utilise', 'action']
    search_fields = ['user__email', 'code']
    readonly_fields = ['cree_le']
