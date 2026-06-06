"""Variables globales injectées dans tous les templates."""
from django.utils import timezone


def site_config(request):
    return {
        'site_name': 'Ventoryx Academy',
        'current_year': timezone.now().year,
        'email_contact': 'contact@ventoryx-academy.com',
        'directeur_publication': 'Directeur Général',
        'hebergeur_nom': None,
        'hebergeur_adresse': None,
        'hebergeur_site': None,
        'hebergeur_localisation': 'Union Européenne',
        'adresse_siege': None,
        'statut_juridique': 'Projet en phase de développement',
        'siret': None,
        'dpo_email': 'dpo@ventoryx-academy.com',
        'age_minimum': 16,
        'slogan': 'Protocole d\'excellence aéronautique',
        'places_bienvenue_restantes': None,
    }


def langue_context(request):
    from apps.core.translation import LANGUES
    return {
        'langues': LANGUES,
        'langue_active': request.session.get('langue', getattr(request, 'LANGUAGE_CODE', 'fr')[:2]),
    }
