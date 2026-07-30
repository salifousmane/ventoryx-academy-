"""
Commande de gestion : initialise les données de test (utilisateurs, parcours, forums).
Lance seed_defaults() indépendamment du nombre d'utilisateurs existants.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialise les données de test Ventoryx Academy'

    def handle(self, *args, **options):
        try:
            from seed import seed_defaults
            seed_defaults()
            self.stdout.write(self.style.SUCCESS('✅ Données initialisées avec succès.'))
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'⚠️  Seed partiel : {e}'))
