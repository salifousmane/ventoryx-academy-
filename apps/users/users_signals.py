"""Signaux : attribution offre bienvenue, vérification âge."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from datetime import timedelta
from .models import User, Subscription


@receiver(post_save, sender=User)
def attribuer_offre_bienvenue(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        count = User.objects.select_for_update().filter(
            date_inscription__lt=instance.date_inscription
        ).count()

        if count == 0:
            instance.is_welcome_tier_1 = True
            instance.save(update_fields=['is_welcome_tier_1'])
            Subscription.objects.create(
                user=instance,
                plan_type='bienvenue_annuel',
                end_date=timezone.now() + timedelta(days=365),
                is_auto_granted=True,
            )
        elif count in [1, 2]:
            instance.is_welcome_tier_2 = True
            instance.save(update_fields=['is_welcome_tier_2'])
            Subscription.objects.create(
                user=instance,
                plan_type='bienvenue_mensuel',
                end_date=timezone.now() + timedelta(days=30),
                is_auto_granted=True,
            )


@receiver(pre_save, sender=User)
def verifier_age_inscription(sender, instance, **kwargs):
    if instance.date_naissance:
        age_min = getattr(settings, 'AGE_MINIMUM', 16)
        today = timezone.now().date()
        age = today.year - instance.date_naissance.year
        if today.month < instance.date_naissance.month or (
            today.month == instance.date_naissance.month and today.day < instance.date_naissance.day
        ):
            age -= 1
        if age < age_min:
            instance.is_active = False
